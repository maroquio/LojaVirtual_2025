from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets
import uvicorn

from repo import usuario_repo
from repo import admin_repo
from repo import cliente_repo
from repo import produto_repo
from repo import forma_pagamento_repo
from repo import categoria_repo

from routes.public_routes import router as public_router
from routes.admin_categorias_routes import router as admin_categorias_router
from routes.admin_produtos_routes import router as admin_produtos_router
from routes.admin_clientes_routes import router as admin_clientes_router
from routes.admin_formas_routes import router as admin_formas_pagamento_router
from routes.auth_routes import router as auth_router
from routes.perfil_routes import router as perfil_router
from routes.admin_usuarios_routes import router as admin_usuarios_router

app = FastAPI()

# Configurar SessionMiddleware com uma chave secreta segura
SECRET_KEY = "LgywzDkuDTHCvW0zW3KELYrNGCyI7C1grkVcLaEP4MelYy7VCgY4b42dJWgOLM3vLPGNX4ig4xHWDoEmPsc0IcGN7DvUNg3mTC04sieAYnERERz0Dn2USgoKrJOyEbDK"

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, defina como True se usar HTTPS
)

app.mount("/static", StaticFiles(directory="static"), name="static")

categoria_repo.criar_tabela()
produto_repo.criar_tabela()
usuario_repo.criar_tabela()
admin_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()

# Criar admin padrão ao inicializar
from util.criar_admin import criar_admin_padrao
criar_admin_padrao()

app.include_router(public_router)
app.include_router(admin_categorias_router, prefix="/admin/categorias")
app.include_router(admin_produtos_router, prefix="/admin/produtos")
app.include_router(admin_clientes_router, prefix="/admin/clientes")
app.include_router(admin_formas_pagamento_router, prefix="/admin/formas")
app.include_router(auth_router)
app.include_router(perfil_router)
app.include_router(admin_usuarios_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
