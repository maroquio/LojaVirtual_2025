from typing import Optional
from data.cliente_model import Cliente
from data.cliente_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(cliente: Cliente) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            cliente.nome, 
            cliente.cpf, 
            cliente.email, 
            cliente.telefone, 
            cliente.senha))
        return cursor.lastrowid

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