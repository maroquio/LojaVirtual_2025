from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    
def inserir(categoria: Categoria) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome,))
        return cursor.lastrowid
    
def obter_todos() -> list[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        categorias = [
            Categoria(id=row["id"], nome=row["nome"])
            for row in rows]
        return categorias
    
def obter_por_id(id: int) -> Optional[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Categoria(id=row["id"], nome=row["nome"])
        return None
    
def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return (cursor.rowcount > 0)
    
def atualizar(categoria: Categoria) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (categoria.nome, categoria.id))
        return (cursor.rowcount > 0)