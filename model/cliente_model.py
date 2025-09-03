from dataclasses import dataclass


@dataclass
class Cliente:
    id: int
    cpf: str
    telefone: str
