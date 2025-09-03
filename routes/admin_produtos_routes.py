from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.produto_model import Produto
from repo import produto_repo, categoria_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/produtos")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "produtos": produtos}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "cadastrar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
    usuario_logado: dict = None
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
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    categorias = categoria_repo.obter_todos()
    if produto:
        response = templates.TemplateResponse(
            "alterar.html",
            {"request": request, "produto": produto, "categorias": categorias},
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
    usuario_logado: dict = None
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
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
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
