from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.categoria_model import Categoria
from repo import categoria_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/categorias")
async def get_categorias():
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse("admin/categorias.html", {"request": {}, "categorias": categorias})
    return response

@router.get("/admin/categorias/cadastrar")
async def get_categoria_cadastrar(request: Request):
    response = templates.TemplateResponse("admin/cadastrar_categoria.html", {"request": request})
    return response

@router.post("/admin/categorias/cadastrar")
async def post_categoria_cadastrar(request: Request, nome: str = Form(...)):
    categoria = Categoria(id=0, nome=nome)
    categoria_id = categoria_repo.inserir(categoria)
    if categoria_id:
        response = RedirectResponse("/admin/categorias", status_code=303)
        return response
    return templates.TemplateResponse("admin/cadastrar_categoria.html", {"request": request, "mensagem": "Erro ao cadastrar categoria."})

@router.get("/admin/categorias/alterar/{id}")
async def get_categoria_alterar(id: int):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse("admin/alterar_categoria.html", {"request": {}, "categoria": categoria})
        return response
    return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Categoria não encontrada."})

@router.post("/admin/categorias/alterar")
async def post_categoria_alterar(
    request: Request,
    id: int = Form(...), 
    nome: str = Form(...)):
    categoria = Categoria(id=id, nome=nome)
    if categoria_repo.atualizar(categoria):
        response = RedirectResponse("/admin/categorias", status_code=303)
        return response
    return templates.TemplateResponse("admin/alterar_categoria.html", {"request": request, "mensagem": "Erro ao alterar categoria."})

@router.get("/admin/categorias/excluir/{id}")
async def get_categoria_excluir(
    request: Request, id: int):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse("admin/excluir_categoria.html", {"request": request, "categoria": categoria})
        return response
    return RedirectResponse("/admin/categorias", status_code=303)

@router.post("/admin/categorias/excluir")
async def post_categoria_excluir(
    request: Request, 
    id: int = Form(...)):
    if categoria_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/categorias", status_code=303)
        return response
    return templates.TemplateResponse("admin/excluir_categoria.html", {"request": request, "mensagem": "Erro ao excluir categoria."})