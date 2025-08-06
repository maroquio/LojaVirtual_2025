from dataclasses import dataclass

from model.usuario_model import Usuario


@dataclass
class Admin(Usuario):
    master: bool
