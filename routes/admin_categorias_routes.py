from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.categoria_model import Categoria
from repo import categoria_repo
from util.template_util import criar_templates


router = APIRouter()
templates = criar_templates("templates/admin/categorias")

@router.get("/")
async def gets():
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": {}, "categorias": categorias}
    )
    return response


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
async def post_cadastrar(request: Request, nome: str = Form(...)):
    categoria = Categoria(id=0, nome=nome)
    categoria_id = categoria_repo.inserir(categoria)
    if categoria_id:
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar categoria."},
    )


@router.get("/alterar/{id}")
async def get_alterar(id: int):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "alterar.html", {"request": {}, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
async def post_alterar(request: Request, id: int = Form(...), nome: str = Form(...)):
    categoria = Categoria(id=id, nome=nome)
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
async def get_excluir(request: Request, id: int):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
async def post_excluir(request: Request, id: int = Form(...)):
    if categoria_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "mensagem": "Erro ao excluir categoria."},
    )
