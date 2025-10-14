from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
    categoria_id: int
    categoria_nome: Optional[str] = None
    foto_principal: Optional[str] = None

    