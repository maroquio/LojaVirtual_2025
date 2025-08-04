from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str