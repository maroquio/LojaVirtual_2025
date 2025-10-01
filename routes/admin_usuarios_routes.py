from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from dtos.usuario_dto import CriarUsuarioDTO, AlterarUsuarioDTO, ExcluirUsuarioDTO
from model.usuario_model import Usuario
from repo import usuario_repo
from util.security import criar_hash_senha
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter(prefix="/admin/usuarios")
templates = criar_templates("templates/admin/usuarios")


@router.get("/lista")
@requer_autenticacao(["admin"])
async def get_lista(request: Request, usuario_logado: dict = None):
    usuarios_admin = usuario_repo.obter_todos_por_perfil("admin")
    return templates.TemplateResponse(
        "lista.html",
        {"request": request, "usuarios": usuarios_admin}
    )


@router.get("/cadastro")
@requer_autenticacao(["admin"])
async def get_cadastro(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request}
    )


@router.post("/cadastro")
@requer_autenticacao(["admin"])
async def post_cadastro(
    request: Request,
    usuario_dto: CriarUsuarioDTO,
    usuario_logado: dict = None
):
    # Verificar se o email já existe
    usuario_existente = usuario_repo.obter_por_email(usuario_dto.email)
    if usuario_existente:
        return RedirectResponse(
            "/admin/usuarios/cadastro?erro=email_existe",
            status.HTTP_303_SEE_OTHER
        )

    # Criar o novo administrador
    senha_hash = criar_hash_senha(usuario_dto.senha)
    usuario = Usuario(
        id=0,
        nome=usuario_dto.nome,
        email=usuario_dto.email,
        senha=senha_hash,
        perfil="admin"
    )
    
    usuario_repo.inserir(usuario)
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )


@router.get("/alterar/{id:int}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )
    
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "usuario": usuario}
    )


@router.post("/alterar/{id:int}")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    id: int,
    usuario_dto: AlterarUsuarioDTO,
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )

    # Verificar se o novo email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_email(usuario_dto.email)
    if usuario_existente and usuario_existente.id != id:
        return RedirectResponse(
            f"/admin/usuarios/alterar/{id}?erro=email_existe",
            status.HTTP_303_SEE_OTHER
        )

    # Atualizar dados
    usuario.nome = usuario_dto.nome
    usuario.email = usuario_dto.email

    # Se uma nova senha foi fornecida, atualizar
    if usuario_dto.senha and usuario_dto.senha.strip():
        senha_hash = criar_hash_senha(usuario_dto.senha)
        usuario.senha = senha_hash
    
    usuario_repo.alterar(usuario)
    
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )


@router.get("/excluir/{id:int}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    # Não permitir auto-exclusão
    if id == usuario_logado['id']:
        return RedirectResponse(
            "/admin/usuarios/lista?erro=auto_exclusao",
            status.HTTP_303_SEE_OTHER
        )
    
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )
    
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "usuario": usuario}
    )


@router.post("/excluir/{id:int}")
@requer_autenticacao(["admin"])
async def post_excluir(
    request: Request, 
    id: int, 
    usuario_logado: dict = None):
    # Não permitir auto-exclusão
    if id == usuario_logado['id']:
        return RedirectResponse(
            "/admin/usuarios/lista?erro=auto_exclusao",
            status.HTTP_303_SEE_OTHER
        )
    
    usuario = usuario_repo.obter_por_id(id)
    if usuario and usuario.perfil == "admin":
        usuario_repo.excluir(usuario)
    
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )