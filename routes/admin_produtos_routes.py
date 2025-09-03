from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.produto_model import Produto
from repo import produto_repo, categoria_repo
from util.template_util import criar_templates


router = APIRouter()
templates = criar_templates("templates/admin/produtos")


@router.get("/")
async def gets():
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": {}, "produtos": produtos}
    )
    return response


@router.get("/detalhar/{id}")
async def get_detalhar(id: int):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": {}, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "cadastrar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.post("/cadastrar")
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
):
    produto = Produto(
        id=0,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        categoria_id=categoria_id,
    )
    produto_id = produto_repo.inserir(produto)
    if produto_id:
        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    categorias = categoria_repo.obter_todos()
    return templates.TemplateResponse(
        "cadastrar.html",
        {
            "request": request,
            "categorias": categorias,
            "mensagem": "Erro ao cadastrar produto.",
        },
    )


@router.get("/alterar/{id}")
async def get_alterar(id: int):
    produto = produto_repo.obter_por_id(id)
    categorias = categoria_repo.obter_todos()
    if produto:
        response = templates.TemplateResponse(
            "alterar.html",
            {"request": {}, "produto": produto, "categorias": categorias},
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
async def post_alterar(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
):
    produto = Produto(
        id=id,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        categoria_id=categoria_id,
    )
    if produto_repo.alterar(produto):
        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    categorias = categoria_repo.obter_todos()
    return templates.TemplateResponse(
        "alterar.html",
        {
            "request": request,
            "produto": produto,
            "categorias": categorias,
            "mensagem": "Erro ao alterar produto.",
        },
    )


@router.get("/excluir/{id}")
async def get_excluir(request: Request, id: int):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
async def post_excluir(request: Request, id: int = Form(...)):
    if produto_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    produto = produto_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {
            "request": request,
            "produto": produto,
            "mensagem": "Erro ao excluir produto.",
        },
    )
