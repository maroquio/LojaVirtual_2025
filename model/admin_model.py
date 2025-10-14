from dataclasses import dataclass
from typing import Optional


@dataclass
class Admin:
    id: int
    master: bool
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
