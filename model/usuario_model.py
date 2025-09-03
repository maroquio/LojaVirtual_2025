from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    perfil: str = 'cliente'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None