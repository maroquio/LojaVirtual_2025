from dataclasses import dataclass


@dataclass
class FormaPagamento:
    id: int
    nome: str
    desconto: float
