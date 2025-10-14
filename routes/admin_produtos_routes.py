from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
import os
from typing import Optional

from dtos.produto_dto import CriarProdutoDTO, AlterarProdutoDTO, ExcluirProdutoDTO, ReordenarFotosDTO
from model.produto_model import Produto
from repo import produto_repo, categoria_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao
from util.foto_util import (
    salvar_nova_foto, obter_foto_principal, obter_todas_fotos,
    excluir_foto, reordenar_fotos, obter_proximo_numero
)


router = APIRouter()
templates = criar_templates("templates/admin/produtos")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: Optional[dict] = None):
    produtos = produto_repo.obter_todos()

    # Adicionar informação de foto para cada produto
    for produto in produtos:
        produto.foto_principal = obter_foto_principal(produto.id)

    response = templates.TemplateResponse(
        "listar.html", {"request": request, "produtos": produtos}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "cadastrar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    produto_dto: CriarProdutoDTO,
    foto: Optional[UploadFile] = File(None),
    usuario_logado: Optional[dict] = None
):
    produto = Produto(
        id=0,
        nome=produto_dto.nome,
        descricao=produto_dto.descricao,
        preco=produto_dto.preco,
        quantidade=produto_dto.quantidade,
        categoria_id=produto_dto.categoria_id,
    )
    produto_id = produto_repo.inserir(produto)
    if produto_id:
        # Salvar foto se foi enviada
        if foto and foto.filename:
            try:
                salvar_nova_foto(produto_id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto: {e}")

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
async def get_alterar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    produto = produto_repo.obter_por_id(id)
    categorias = categoria_repo.obter_todos()
    if produto:
        foto_principal = obter_foto_principal(id)
        response = templates.TemplateResponse(
            "alterar.html",
            {
                "request": request,
                "produto": produto,
                "categorias": categorias,
                "foto_principal": foto_principal
            },
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    produto_dto: AlterarProdutoDTO,
    foto: Optional[UploadFile] = File(None),
    usuario_logado: Optional[dict] = None
):
    produto = Produto(
        id=produto_dto.id,
        nome=produto_dto.nome,
        descricao=produto_dto.descricao,
        preco=produto_dto.preco,
        quantidade=produto_dto.quantidade,
        categoria_id=produto_dto.categoria_id,
    )
    if produto_repo.alterar(produto):
        # Salvar nova foto se foi enviada
        if foto and foto.filename:
            try:
                salvar_nova_foto(produto_dto.id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto: {e}")

        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    categorias = categoria_repo.obter_todos()
    foto_principal = obter_foto_principal(produto_dto.id)
    return templates.TemplateResponse(
        "alterar.html",
        {
            "request": request,
            "produto": produto,
            "categorias": categorias,
            "foto_principal": foto_principal,
            "mensagem": "Erro ao alterar produto.",
        },
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, produto_dto: ExcluirProdutoDTO, usuario_logado: Optional[dict] = None):
    if produto_repo.excluir_por_id(produto_dto.id):
        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    produto = produto_repo.obter_por_id(produto_dto.id)
    return templates.TemplateResponse(
        "excluir.html",
        {
            "request": request,
            "produto": produto,
            "mensagem": "Erro ao excluir produto.",
        },
    )


@router.get("/{id}/galeria")
@requer_autenticacao(["admin"])
async def get_galeria(request: Request, id: int, usuario_logado: Optional[dict] = None):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    fotos = obter_todas_fotos(id)
    response = templates.TemplateResponse(
        "galeria.html",
        {
            "request": request,
            "produto": produto,
            "fotos": fotos
        }
    )
    return response


@router.post("/{id}/galeria/upload")
@requer_autenticacao(["admin"])
async def post_galeria_upload(
    request: Request,
    id: int,
    fotos: list[UploadFile] = File(...),
    usuario_logado: Optional[dict] = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    sucesso = 0
    for foto in fotos:
        if foto.filename:
            try:
                salvar_nova_foto(id, foto.file, como_principal=False)
                sucesso += 1
            except Exception as e:
                print(f"Erro ao salvar foto {foto.filename}: {e}")

    # Adicionar mensagem de sucesso via session ou query param
    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)


@router.post("/{id}/galeria/excluir/{numero}")
@requer_autenticacao(["admin"])
async def post_galeria_excluir(
    request: Request,
    id: int,
    numero: int,
    usuario_logado: Optional[dict] = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        excluir_foto(id, numero)
    except Exception as e:
        print(f"Erro ao excluir foto: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)


@router.post("/{id}/galeria/reordenar")
@requer_autenticacao(["admin"])
async def post_galeria_reordenar(
    request: Request,
    id: int,
    reordenar_dto: ReordenarFotosDTO,
    usuario_logado: Optional[dict] = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        # Converter string de números separados por vírgula em lista de inteiros
        ordem_lista = [int(x.strip()) for x in reordenar_dto.nova_ordem.split(",")]
        reordenar_fotos(id, ordem_lista)
    except Exception as e:
        print(f"Erro ao reordenar fotos: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)
