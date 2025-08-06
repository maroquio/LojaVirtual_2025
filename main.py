from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from data import produto_repo
from data import cliente_repo
from data import forma_pagamento_repo

from routes.admin.admin_produto_routes import router as admin_produtos_router
from routes.admin.admin_cliente_routes import router as admin_clientes_router
from routes.admin.admin_formas_routes import router as admin_formas_pagamento_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

produto_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()

app.include_router(admin_produtos_router)
app.include_router(admin_clientes_router)
app.include_router(admin_formas_pagamento_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)