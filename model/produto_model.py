from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int

    