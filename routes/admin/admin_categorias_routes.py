from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from model.categoria_model import Categoria
from repo import categoria_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/categorias/listar")
async def get_categorias():
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "categorias": categorias})
    return response

@router.get("/admin/categorias/cadastrar")
async def get_categoria_cadastrar():
    response = templates.TemplateResponse("admin/cadastrar_categoria.html", {"request": {}})
    return response

@router.post("/admin/categorias/cadastrar")
async def post_categoria_cadastrar(nome: str):
    categoria = Categoria(id=0, nome=nome)
    categoria_id = categoria_repo.inserir(categoria)
    if categoria_id:
        return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Categoria cadastrada com sucesso!"})
    return templates.TemplateResponse("admin/cadastrar_categoria.html", {"request": {}, "mensagem": "Erro ao cadastrar categoria."})

@router.get("/admin/categorias/alterar/{id}")
async def get_categoria_alterar(id: int):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse("admin/alterar_categoria.html", {"request": {}, "categoria": categoria})
        return response
    return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Categoria não encontrada."})

@router.post("/admin/categorias/alterar")
async def post_categoria_alterar(id: int, nome: str):
    categoria = Categoria(id=id, nome=nome)
    if categoria_repo.atualizar(categoria):
        return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Categoria alterada com sucesso!"})
    return templates.TemplateResponse("admin/alterar_categoria.html", {"request": {}, "mensagem": "Erro ao alterar categoria."})

@router.get("/admin/categorias/excluir/{id}")
async def get_categoria_excluir(id: int):
    if categoria_repo.excluir_por_id(id):
        return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Categoria excluída com sucesso!"})
    return templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "mensagem": "Erro ao excluir categoria."})

@router.get("/admin/categorias")
async def get_admin_categorias():
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse("admin/listar_categorias.html", {"request": {}, "categorias": categorias})
    return response