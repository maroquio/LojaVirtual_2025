from typing import Optional, Annotated
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from dtos.auth_dto import LoginDTO, CadastroPublicoDTO, EsqueciSenhaDTO, RedefinirSenhaDTO
from model.usuario_model import Usuario
from model.cliente_model import Cliente
from repo import usuario_repo
from util.email_service import email_service
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token, validar_forca_senha
from util.auth_decorator import criar_sessao, destruir_sessao, esta_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/auth")


@router.get("/login")
async def get_login(request: Request, redirect: Optional[str] = None):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "redirect": redirect}
    )


@router.post("/login")
async def post_login(
    request: Request,
    email: Annotated[str, Form()],
    senha: Annotated[str, Form()],
    redirect: str = Form(None)
):
    # Validar dados com DTO
    try:
        login_dto = LoginDTO(email=email, senha=senha)
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erro": str(e),
                "email": email,
                "redirect": redirect
            }
        )
    
    # Buscar usuário pelo email
    usuario = usuario_repo.obter_por_email(login_dto.email)

    if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erro": "Email ou senha inválidos",
                "email": login_dto.email,
                "redirect": redirect
            }
        )

    # Criar sessão
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)

    # Redirecionar para a página solicitada ou home
    url_redirect = redirect if redirect else "/"
    return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request):
    destruir_sessao(request)
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("cadastro.html", {"request": request})


@router.post("/cadastro")
async def post_cadastro(
    request: Request,
    nome: Annotated[str, Form()],
    email: Annotated[str, Form()],
    cpf: Annotated[str, Form()],
    telefone: Annotated[str, Form()],
    senha: Annotated[str, Form()],
    confirmar_senha: Annotated[str, Form()]
):
    # Validar dados com DTO
    try:
        cadastro_dto = CadastroPublicoDTO(
            nome=nome,
            email=email,
            cpf=cpf,
            telefone=telefone,
            senha=senha,
            confirmar_senha=confirmar_senha
        )
    except Exception as e:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": str(e),
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone
            }
        )
    
    # Validações já feitas pelo DTO (incluindo coincidência de senhas)

    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(cadastro_dto.senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": msg_erro,
                "nome": cadastro_dto.nome,
                "email": cadastro_dto.email,
                "cpf": cadastro_dto.cpf,
                "telefone": cadastro_dto.telefone
            }
        )

    # Verificar se email já existe
    if usuario_repo.obter_por_email(cadastro_dto.email):
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": "Este email já está cadastrado",
                "nome": cadastro_dto.nome,
                "cpf": cadastro_dto.cpf,
                "telefone": cadastro_dto.telefone
            }
        )

    try:
        # Criar usuário com senha hash
        usuario = Usuario(
            id=0,
            nome=cadastro_dto.nome,
            email=cadastro_dto.email,
            senha=criar_hash_senha(cadastro_dto.senha),
            perfil='cliente'
        )

        # Inserir usuário e cliente
        from util.db_util import get_connection
        with get_connection() as conn:
            cursor = conn.cursor()

            # Inserir usuário
            usuario_id = usuario_repo.inserir(usuario, cursor)
            if not usuario_id:
                raise Exception("Erro ao inserir usuário")

            # Inserir dados do cliente
            cliente = Cliente(
                id=usuario_id,
                cpf=cadastro_dto.cpf,
                telefone=cadastro_dto.telefone
            )
            cursor.execute(
                "INSERT INTO cliente (id, cpf, telefone) VALUES (?, ?, ?)",
                (cliente.id, cliente.cpf, cliente.telefone)
            )

            conn.commit()

        # Fazer login automático após cadastro
        usuario_dict = {
            "id": usuario_id,
            "nome": cadastro_dto.nome,
            "email": cadastro_dto.email,
            "perfil": 'cliente',
            "foto": None
        }
        criar_sessao(request, usuario_dict)
        email_service.enviar_boas_vindas(
            para_email=cadastro_dto.email,
            para_nome=cadastro_dto.nome
        )
        return RedirectResponse("/perfil", status.HTTP_303_SEE_OTHER)

    except Exception as e:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": f"Erro ao criar cadastro. Tente novamente. {e}",
                "nome": cadastro_dto.nome,
                "email": cadastro_dto.email,
                "cpf": cadastro_dto.cpf,
                "telefone": cadastro_dto.telefone
            }
        )


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})


@router.post("/esqueci-senha")
async def post_esqueci_senha(
    request: Request,
    email: Annotated[str, Form()]
):
    # Validar dados com DTO
    try:
        esqueci_dto = EsqueciSenhaDTO(email=email)
    except Exception as e:
        return templates.TemplateResponse(
            "esqueci_senha.html",
            {
                "request": request,
                "erro": str(e)
            }
        )
    
    usuario = usuario_repo.obter_por_email(esqueci_dto.email)

    # Sempre mostrar mensagem de sucesso por segurança (não revelar emails válidos)
    mensagem_sucesso = "Se o email estiver cadastrado, você receberá instruções para redefinir sua senha."

    if usuario:
        # Gerar token e salvar no banco
        token = gerar_token_redefinicao()
        data_expiracao = obter_data_expiracao_token(24)  # 24 horas
        usuario_repo.atualizar_token(esqueci_dto.email, token, data_expiracao)

        # TODO: Enviar email com o link de redefinição
        # Por enquanto, vamos apenas mostrar o link (em produção, remover isso)
        link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"

        return templates.TemplateResponse(
            "esqueci_senha.html",
            {
                "request": request,
                "sucesso": mensagem_sucesso,
                "debug_link": link_redefinicao  # Remover em produção
            }
        )

    return templates.TemplateResponse(
        "esqueci_senha.html",
        {
            "request": request,
            "sucesso": mensagem_sucesso
        }
    )


@router.get("/redefinir-senha/{token}")
async def get_redefinir_senha(request: Request, token: str):
    usuario = usuario_repo.obter_por_token(token)

    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )

    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/redefinir-senha/{token}")
async def post_redefinir_senha(
    request: Request,
    token: str,
    senha: Annotated[str, Form()],
    confirmar_senha: Annotated[str, Form()]
):
    usuario = usuario_repo.obter_por_token(token)

    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )

    # Validar dados com DTO
    try:
        redefinir_dto = RedefinirSenhaDTO(senha=senha, confirmar_senha=confirmar_senha)
    except Exception as e:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": str(e)
            }
        )
    
    # Validações já feitas pelo DTO (senhas coincidem)

    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(redefinir_dto.senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": msg_erro
            }
        )

    # Atualizar senha e limpar token
    senha_hash = criar_hash_senha(redefinir_dto.senha)
    usuario_repo.atualizar_senha(usuario.id, senha_hash)
    usuario_repo.limpar_token(usuario.id)

    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "sucesso": "Senha redefinida com sucesso! Você já pode fazer login."
        }
    )
