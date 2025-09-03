from typing import Optional
from model.produto_model import Produto
from sql.produto_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produto'")
        tabela_existe = cursor.fetchone() is not None
        
        if tabela_existe:
            # Verifica se a coluna categoria_id existe
            cursor.execute("PRAGMA table_info(produto)")
            colunas = cursor.fetchall()
            tem_categoria = any(col[1] == 'categoria_id' for col in colunas)
            
            if not tem_categoria:
                try:
                    # Adiciona a coluna categoria_id com valor padrão 1
                    cursor.execute("ALTER TABLE produto ADD COLUMN categoria_id INTEGER DEFAULT 1")
                    conn.commit()
                except:
                    pass
        else:
            # Cria a tabela nova com categoria_id
            cursor.execute(CRIAR_TABELA)
        
        return True

def inserir(produto: Produto) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            produto.nome, 
            produto.descricao, 
            produto.preco, 
            produto.quantidade,
            produto.categoria_id))
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
                quantidade=row["quantidade"],
                categoria_id=row["categoria_id"],
                categoria_nome=row["categoria_nome"])
            for row in rows]
        return produtos
    
def obter_por_id(id: int) -> Optional[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            produto = Produto(
                id=row["id"], 
                nome=row["nome"], 
                descricao=row["descricao"], 
                preco=row["preco"], 
                quantidade=row["quantidade"],
                categoria_id=row["categoria_id"],
                categoria_nome=row["categoria_nome"])
            return produto
        return None
    

def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return (cursor.rowcount > 0)

def alterar(produto: Produto) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.quantidade,
            produto.categoria_id,
            produto.id))
        return cursor.rowcount > 0