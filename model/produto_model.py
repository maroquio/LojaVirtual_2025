from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
    categoria_id: int
    categoria_nome: str = None

    