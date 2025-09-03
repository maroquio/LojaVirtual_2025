import os
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from model.usuario_model import Usuario
from model.cliente_model import Cliente
from repo import usuario_repo, cliente_repo
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/perfil")


@router.get("/perfil")
@requer_autenticacao()
async def get_perfil(request: Request, usuario_logado: dict = None):
    # Buscar dados completos do usuário
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Se for cliente, buscar dados adicionais
    cliente_dados = None
    if usuario.perfil == 'cliente':
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT cpf, telefone FROM cliente WHERE id=?", (usuario.id,))
                row = cursor.fetchone()
                if row:
                    cliente_dados = {
                        'cpf': row['cpf'],
                        'telefone': row['telefone']
                    }
        except:
            pass
    
    return templates.TemplateResponse(
        "dados.html",
        {
            "request": request,
            "usuario": usuario,
            "cliente_dados": cliente_dados
        }
    )


@router.post("/perfil")
@requer_autenticacao()
async def post_perfil(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(None),
    telefone: str = Form(None),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Verificar se o email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_email(email)
    if usuario_existente and usuario_existente.id != usuario.id:
        cliente_dados = None
        if usuario.perfil == 'cliente':
            try:
                from util.db_util import get_connection
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT cpf, telefone FROM cliente WHERE id=?", (usuario.id,))
                    row = cursor.fetchone()
                    if row:
                        cliente_dados = {
                            'cpf': row['cpf'],
                            'telefone': row['telefone']
                        }
            except:
                pass
        
        return templates.TemplateResponse(
            "dados.html",
            {
                "request": request,
                "usuario": usuario,
                "cliente_dados": cliente_dados,
                "erro": "Este email já está em uso"
            }
        )
    
    # Atualizar dados do usuário
    usuario.nome = nome
    usuario.email = email
    usuario_repo.alterar(usuario)
    
    # Se for cliente, atualizar dados adicionais
    if usuario.perfil == 'cliente' and cpf and telefone:
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE cliente SET cpf=?, telefone=? WHERE id=?",
                    (cpf, telefone, usuario.id)
                )
                conn.commit()
        except:
            pass
    
    # Atualizar sessão
    from util.auth_decorator import criar_sessao
    usuario_dict = {
        "id": usuario.id,
        "nome": nome,
        "email": email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    return RedirectResponse("/perfil?sucesso=1", status.HTTP_303_SEE_OTHER)


@router.get("/perfil/alterar-senha")
@requer_autenticacao()
async def get_alterar_senha(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "alterar_senha.html",
        {"request": request}
    )


@router.post("/perfil/alterar-senha")
@requer_autenticacao()
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    senha_nova: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Verificar senha atual
    if not verificar_senha(senha_atual, usuario.senha):
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "Senha atual incorreta"
            }
        )
    
    # Verificar se as novas senhas coincidem
    if senha_nova != confirmar_senha:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "As novas senhas não coincidem"
            }
        )
    
    # Validar força da nova senha
    senha_valida, msg_erro = validar_forca_senha(senha_nova)
    if not senha_valida:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha
    senha_hash = criar_hash_senha(senha_nova)
    usuario_repo.atualizar_senha(usuario.id, senha_hash)
    
    return templates.TemplateResponse(
        "alterar_senha.html",
        {
            "request": request,
            "sucesso": "Senha alterada com sucesso!"
        }
    )


@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)
    
    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único para o arquivo
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)
    
    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
        
        # Atualizar caminho no banco
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)
        
        # Atualizar sessão
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)
        
    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)