from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from repo import produto_repo, usuario_repo, cliente_repo, forma_pagamento_repo, categoria_repo
from routes.admin.categoria_routes import router as admin_categoria_router
from routes.admin.produto_routes import router as admin_produto_router
from routes.public_routes import router as public_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


categoria_repo.criar_tabela()
produto_repo.criar_tabela()
usuario_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()


app.include_router(public_router)
app.include_router(admin_categoria_router)
app.include_router(admin_produto_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)