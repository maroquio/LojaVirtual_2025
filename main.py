from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from repo import usuario_repo
from repo import admin_repo
from repo import cliente_repo
from repo import produto_repo
from repo import forma_pagamento_repo
from repo import categoria_repo

from routes.public_routes import router as public_routes
from routes.admin.admin_categorias_routes import router as admin_categorias_router
from routes.admin.admin_produtos_routes import router as admin_produtos_router
from routes.admin.admin_clientes_routes import router as admin_clientes_router
from routes.admin.admin_formas_routes import router as admin_formas_pagamento_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

categoria_repo.criar_tabela()
produto_repo.criar_tabela()
usuario_repo.criar_tabela()
admin_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()

app.include_router(public_routes)
app.include_router(admin_categorias_router)
app.include_router(admin_produtos_router)
app.include_router(admin_clientes_router)
app.include_router(admin_formas_pagamento_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)