from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from repo import produto_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root():
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse("index.html", {"request": {}, "produtos": produtos})
    return response