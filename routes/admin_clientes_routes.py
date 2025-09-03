from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.cliente_model import Cliente
from repo import cliente_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/clientes")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "clientes": clientes}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: dict = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    cliente = Cliente(
        id=0,
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        senha=senha
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
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
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
    id: int = Form(...),
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(None),
    usuario_logado: dict = None
):
    # Se a senha não foi fornecida, buscar a senha atual
    if not senha:
        cliente_atual = cliente_repo.obter_por_id(id)
        senha = cliente_atual.senha if cliente_atual else ""
    
    cliente = Cliente(
        id=id,
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
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
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if cliente_repo.excluir(id):
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    cliente = cliente_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao excluir cliente."},
    )