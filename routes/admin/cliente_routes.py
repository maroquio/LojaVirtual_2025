from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from repo import cliente_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/clientes")
async def get_clientes():
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse("admin/listar_clientes.html", {"request": {}, "clientes": clientes})
    return response