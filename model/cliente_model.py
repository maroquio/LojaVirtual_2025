from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: int
    cpf: str
    telefone: str
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
