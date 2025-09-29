from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from repo import produto_repo
from util.foto_util import obter_foto_principal, obter_todas_fotos


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


@router.get("/produtos/{id}")
async def get_produto_detalhes(request: Request, id: int):
    produto = produto_repo.obter_por_id(id)

    if not produto:
        return RedirectResponse("/", status_code=302)

    # Obter todas as fotos do produto para a galeria
    fotos = obter_todas_fotos(id)

    # Se não há fotos, usar placeholder
    if not fotos:
        fotos = ["/static/img/placeholder.png"]

    response = templates.TemplateResponse(
        "produto_detalhes.html",
        {
            "request": request,
            "produto": produto,
            "fotos": fotos
        }
    )
    return response