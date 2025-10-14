from typing import Optional
from repo import usuario_repo
from model.cliente_model import Cliente
from sql.cliente_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(cliente: Cliente) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        assert cliente.nome is not None, "Nome do cliente é obrigatório"
        assert cliente.email is not None, "Email do cliente é obrigatório"
        assert cliente.senha is not None, "Senha do cliente é obrigatória"
        usuario = Usuario(0,
            cliente.nome,
            cliente.email,
            cliente.senha)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            id_usuario,
            cliente.cpf,
            cliente.telefone))
        return id_usuario

def alterar(cliente: Cliente) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        assert cliente.nome is not None, "Nome do cliente é obrigatório"
        assert cliente.email is not None, "Email do cliente é obrigatório"
        assert cliente.senha is not None, "Senha do cliente é obrigatória"
        usuario = Usuario(cliente.id,
            cliente.nome,
            cliente.email,
            cliente.senha)
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (
            cliente.cpf,
            cliente.telefone,
            cliente.id))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)

def obter_por_id(id: int) -> Optional[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        cliente = Cliente(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            email=row["email"],
            telefone=row["telefone"],
            senha=row["senha"])
        return cliente
    
def obter_todos() -> list[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        clientes = [
            Cliente(
                id=row["id"], 
                nome=row["nome"], 
                cpf=row["cpf"],
                email=row["email"],
                telefone=row["telefone"],
                senha=row["senha"]) 
                for row in rows]
        return clientes