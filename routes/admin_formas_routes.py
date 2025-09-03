from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.forma_pagamento_model import FormaPagamento
from repo import forma_pagamento_repo
from util.template_util import criar_templates


router = APIRouter()
templates = criar_templates("templates/admin/formas")


@router.get("/")
async def gets():
    formas = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse(
        "listar.html", {"request": {}, "formas": formas}
    )
    return response


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
async def post_cadastrar(request: Request, nome: str = Form(...), desconto: float = Form(...)):
    forma = FormaPagamento(id=0, nome=nome, desconto=desconto)
    forma_id = forma_pagamento_repo.inserir(forma)
    if forma_id:
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar forma de pagamento."},
    )


@router.get("/alterar/{id}")
async def get_alterar(id: int):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "alterar.html", {"request": {}, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
async def post_alterar(request: Request, id: int = Form(...), nome: str = Form(...), desconto: float = Form(...)):
    forma = FormaPagamento(id=id, nome=nome, desconto=desconto)
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
async def get_excluir(request: Request, id: int):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
async def post_excluir(request: Request, id: int = Form(...)):
    if forma_pagamento_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    forma = forma_pagamento_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "forma": forma, "mensagem": "Erro ao excluir forma de pagamento."},
    )