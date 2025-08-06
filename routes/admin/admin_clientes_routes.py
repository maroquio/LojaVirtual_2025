from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates

from repo import cliente_repo


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/admin/clientes")
async def get_clientes():
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse("clientes.html", {"request": {}, "clientes": clientes})
    return response