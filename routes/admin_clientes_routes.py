from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.cliente_model import Cliente
from repo import cliente_repo
from util.template_util import criar_templates


router = APIRouter()
templates = criar_templates("templates/admin/clientes")


@router.get("/")
async def gets():
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": {}, "clientes": clientes}
    )
    return response


@router.get("/detalhar/{id}")
async def get_detalhar(id: int):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": {}, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
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
async def get_alterar(id: int):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "alterar.html", {"request": {}, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
async def post_alterar(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(None),
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
async def get_excluir(request: Request, id: int):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
async def post_excluir(request: Request, id: int = Form(...)):
    if cliente_repo.excluir(id):
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    cliente = cliente_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao excluir cliente."},
    )