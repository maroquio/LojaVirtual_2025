"""
Exceções customizadas da aplicação
"""

class LojaVirtualError(Exception):
    """Exceção base para erros da aplicação"""
    def __init__(self, mensagem: str, erro_original: Exception = None):
        self.mensagem = mensagem
        self.erro_original = erro_original
        super().__init__(self.mensagem)


class ValidacaoError(LojaVirtualError):
    """Erro de validação de dados"""
    def __init__(self, mensagem: str, campo: str = None, valor: any = None):
        super().__init__(mensagem)
        self.campo = campo
        self.valor = valor


class RecursoNaoEncontradoError(LojaVirtualError):
    """Erro quando um recurso não é encontrado"""
    def __init__(self, recurso: str, identificador: any):
        mensagem = f"{recurso} não encontrado: {identificador}"
        super().__init__(mensagem)
        self.recurso = recurso
        self.identificador = identificador


class BancoDadosError(LojaVirtualError):
    """Erro relacionado ao banco de dados"""
    def __init__(self, mensagem: str, operacao: str, erro_original: Exception = None):
        super().__init__(mensagem, erro_original)
        self.operacao = operacao