from typing import Optional
from repo import usuario_repo
from model.admin_model import Admin
from sql.admin_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(admin: Admin) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            admin.nome, 
            admin.email, 
            admin.senha)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            id_usuario,
            admin.master))
        return id_usuario
    
def alterar(admin: Admin) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(admin.id, 
            admin.nome, 
            admin.email, 
            admin.senha)
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (
            admin.master,
            admin.id))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)

def obter_por_id(id: int) -> Optional[Admin]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        admin = Admin(
            id=row["id"],
            nome=row["nome"],            
            email=row["email"],
            senha=row["senha"],
            master=row["master"])
        return admin
    
def obter_todos() -> list[Admin]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        admins = [
            Admin(
                id=row["id"],
                nome=row["nome"],            
                email=row["email"],
                senha=row["senha"],
                master=row["master"]) 
                for row in rows]
        return admins