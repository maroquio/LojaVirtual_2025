from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from dtos.forma_pagamento_dto import CriarFormaPagamentoDTO, AlterarFormaPagamentoDTO, ExcluirFormaPagamentoDTO
from model.forma_pagamento_model import FormaPagamento
from repo import forma_pagamento_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/formas")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: Optional[dict] = None):
    formas = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "formas": formas}
    )
    return response


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(request: Request, forma_dto: CriarFormaPagamentoDTO, usuario_logado: Optional[dict] = None):
    forma = FormaPagamento(id=0, nome=forma_dto.nome, desconto=forma_dto.desconto)
    forma_id = forma_pagamento_repo.inserir(forma)
    if forma_id:
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar forma de pagamento."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(request: Request, forma_dto: AlterarFormaPagamentoDTO, usuario_logado: Optional[dict] = None):
    forma = FormaPagamento(id=forma_dto.id, nome=forma_dto.nome, desconto=forma_dto.desconto)
    if forma_pagamento_repo.atualizar(forma):
        response = RedirectResponse(
            "/admin/formas", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "forma": forma, "mensagem": "Erro ao alterar forma de pagamento."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, forma_dto: ExcluirFormaPagamentoDTO, usuario_logado: Optional[dict] = None):
    if forma_pagamento_repo.excluir_por_id(forma_dto.id):
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    forma = forma_pagamento_repo.obter_por_id(forma_dto.id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "forma": forma, "mensagem": "Erro ao excluir forma de pagamento."},
    )