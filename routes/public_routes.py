from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from repo import produto_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})
    return response