from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from repo import produto_repo
from util.foto_util import obter_foto_principal


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    produtos = produto_repo.obter_todos()

    # Adicionar informação de foto para cada produto
    for produto in produtos:
        produto.foto_principal = obter_foto_principal(produto.id)

    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})
    return response