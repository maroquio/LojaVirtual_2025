from dataclasses import dataclass

from data.usuario_model import Usuario


@dataclass
class Cliente(Usuario):
    cpf: str
    telefone: str
