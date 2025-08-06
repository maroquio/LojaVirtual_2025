from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data import produto_repo
from model.produto_model import Produto

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/admin/produtos")
async def get_produtos():
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse("produtos.html", {"request": {}, "produtos": produtos})
    return response


@router.get("/admin/produtos/{id}")
async def get_produto_por_id(id: int):
    produto = produto_repo.obter_por_id(id)
    response = templates.TemplateResponse("produto.html", {"request": {}, "produto": produto})
    return response


@router.get("/admin/produtos/cadastrar")
async def get_produto_cadastrar():
    response = templates.TemplateResponse("cadastrar_produto.html", {"request": {}})
    return response


@router.post("/admin/produtos/cadastrar")
async def post_produto_cadastrar(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...)
):
    produto = Produto(0, nome, descricao, preco, quantidade)
    id_produto = produto_repo.inserir(produto)
    if id_produto == None:
        raise Exception("Erro ao inserir produto.")
    else:
        return RedirectResponse("/admin/produtos", status_code=303)


@router.get("/admin/produtos/excluir/{id}")
async def get_excluir_produto(id: int):
    if produto_repo.excluir_por_id(id):
        return RedirectResponse("/admin/produtos", status_code=303)