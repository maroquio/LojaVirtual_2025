from dataclasses import dataclass

from model.usuario_model import Usuario


@dataclass
class Cliente(Usuario):
    cpf: str
    telefone: str
