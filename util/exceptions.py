"""
Exceções customizadas da aplicação
"""
from typing import Any, Optional


class LojaVirtualError(Exception):
    """Exceção base para erros da aplicação"""
    def __init__(self, mensagem: str, erro_original: Optional[Exception] = None):
        self.mensagem = mensagem
        self.erro_original = erro_original
        super().__init__(self.mensagem)


class ValidacaoError(LojaVirtualError):
    """Erro de validação de dados"""
    def __init__(self, mensagem: str, campo: Optional[str] = None, valor: Any = None):
        super().__init__(mensagem)
        self.campo = campo
        self.valor = valor


class RecursoNaoEncontradoError(LojaVirtualError):
    """Erro quando um recurso não é encontrado"""
    def __init__(self, recurso: str, identificador: Any):
        mensagem = f"{recurso} não encontrado: {identificador}"
        super().__init__(mensagem)
        self.recurso = recurso
        self.identificador = identificador


class BancoDadosError(LojaVirtualError):
    """Erro relacionado ao banco de dados"""
    def __init__(self, mensagem: str, operacao: str, erro_original: Optional[Exception] = None):
        super().__init__(mensagem, erro_original)
        self.operacao = operacao