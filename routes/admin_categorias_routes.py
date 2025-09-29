from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from dtos.categoria_dto import AlterarCategoriaDTO, CriarCategoriaDTO
from model.categoria_model import Categoria
from repo import categoria_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/categorias")

@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request, 
    categoria_dto: CriarCategoriaDTO, 
    usuario_logado: dict = None):
    categoria = Categoria(id=0, nome=categoria_dto.nome)
    categoria_id = categoria_repo.inserir(categoria)
    if categoria_id:
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar categoria."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request, 
    categoria_dto: AlterarCategoriaDTO, 
    usuario_logado: dict = None):
    categoria = Categoria(id=categoria_dto.id, nome=categoria_dto.nome)
    if categoria_repo.atualizar(categoria):
        response = RedirectResponse(
            "/admin/categorias", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "mensagem": "Erro ao alterar categoria."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if categoria_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "mensagem": "Erro ao excluir categoria."},
    )
