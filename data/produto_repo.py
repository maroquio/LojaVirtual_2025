from typing import Optional
from data.produto_model import Produto
from data.produto_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(produto: Produto) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            produto.nome, 
            produto.descricao, 
            produto.preco, 
            produto.quantidade))
        return cursor.lastrowid

def obter_todos() -> list[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        produtos = [
            Produto(
                id=row["id"], 
                nome=row["nome"], 
                descricao=row["descricao"], 
                preco=row["preco"], 
                quantidade=row["quantidade"])
            for row in rows]
        return produtos
    
def obter_por_id(id: int) -> Optional[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        produto = Produto(
            id=row["id"], 
            nome=row["nome"], 
            descricao=row["descricao"], 
            preco=row["preco"], 
            quantidade=row["quantidade"])
        return produto