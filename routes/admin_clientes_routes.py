from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from dtos.cliente_dto import CriarClienteDTO, AlterarClienteDTO, ExcluirClienteDTO
from model.cliente_model import Cliente
from repo import cliente_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/clientes")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: Optional[dict] = None):
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "clientes": clientes}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    cliente_dto: CriarClienteDTO,
    usuario_logado: Optional[dict] = None
):
    cliente = Cliente(
        id=0,
        nome=cliente_dto.nome,
        cpf=cliente_dto.cpf,
        email=cliente_dto.email,
        telefone=cliente_dto.telefone,
        senha=cliente_dto.senha
    )
    cliente_id = cliente_repo.inserir(cliente)
    if cliente_id:
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar cliente."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    cliente_dto: AlterarClienteDTO,
    usuario_logado: Optional[dict] = None
):
    # Se a senha não foi fornecida, buscar a senha atual
    senha = cliente_dto.senha
    if not senha or not senha.strip():
        cliente_atual = cliente_repo.obter_por_id(cliente_dto.id)
        senha = cliente_atual.senha if cliente_atual else ""

    cliente = Cliente(
        id=cliente_dto.id,
        nome=cliente_dto.nome,
        cpf=cliente_dto.cpf,
        email=cliente_dto.email,
        telefone=cliente_dto.telefone,
        senha=senha
    )
    if cliente_repo.alterar(cliente):
        response = RedirectResponse(
            "/admin/clientes", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao alterar cliente."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, cliente_dto: ExcluirClienteDTO, usuario_logado: Optional[dict] = None):
    if cliente_repo.excluir(cliente_dto.id):
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    cliente = cliente_repo.obter_por_id(cliente_dto.id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao excluir cliente."},
    )