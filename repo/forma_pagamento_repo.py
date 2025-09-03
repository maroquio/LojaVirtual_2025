from typing import Optional
from model.forma_pagamento_model import FormaPagamento
from sql.forma_pagamento_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0


def inserir(forma_pagamento: FormaPagamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            forma_pagamento.nome, 
            forma_pagamento.desconto))
        id_inserido = cursor.lastrowid
        return id_inserido


def obter_todas() -> list[FormaPagamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [FormaPagamento(
            id=row["id"], 
            nome=row["nome"], 
            desconto=row["desconto"])
            for row in rows]


def obter_por_id(id: int) -> Optional[FormaPagamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return FormaPagamento(
                id=row["id"],
                nome=row["nome"],
                desconto=row["desconto"]
            )
        return None


def atualizar(forma_pagamento: FormaPagamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            forma_pagamento.nome,
            forma_pagamento.desconto,
            forma_pagamento.id
        ))
        return cursor.rowcount > 0


def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return cursor.rowcount > 0
