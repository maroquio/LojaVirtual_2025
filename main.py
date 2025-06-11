from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from data import produto_repo
from data import cliente_repo
from data import forma_pagamento_repo
from data.produto_model import Produto


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

produto_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()


@app.get("/")
async def get_root():
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse("index.html", {"request": {}, "produtos": produtos})
    return response


@app.get("/admin/produtos")
async def get_produtos():
    produtos = produto_repo.obter_todos()
    response = templates.TemplateResponse("produtos.html", {"request": {}, "produtos": produtos})
    return response


@app.get("/produtos/{id}")
async def get_produto_por_id(id: int):
    produto = produto_repo.obter_por_id(id)
    response = templates.TemplateResponse("produto.html", {"request": {}, "produto": produto})
    return response


@app.get("/admin/produtos/cadastrar")
async def get_produto_cadastrar():
    response = templates.TemplateResponse("cadastrar_produto.html", {"request": {}})
    return response


@app.post("/admin/produtos/cadastrar")
async def post_produto_cadastrar(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...)
):
    produto = Produto(0, nome, descricao, preco, quantidade)
    id_produto = produto_repo.inserir(produto)
    if id_produto == None:
        raise Exception("Erro ao inserir produto.")
    else:
        return RedirectResponse("/produtos", status_code=303)


@app.get("/admin/clientes")
async def get_clientes():
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse("clientes.html", {"request": {}, "clientes": clientes})
    return response


@app.get("/admin/formas_pagamento")
async def get_formas_pagamento():
    formas_pagamento = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse("formas_pagamento.html", {"request": {}, "formas_pagamento": formas_pagamento})
    return response


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)