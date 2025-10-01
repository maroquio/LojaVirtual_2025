"""
Sistema de Notificações Toast
Inspirado no sistema de flash messages do projeto CaseBem

Este módulo fornece funções para adicionar notificações toast
que aparecem temporariamente na tela do usuário.
"""

from fastapi import Request
from typing import Optional, List, Dict


class ToastType:
    """Tipos de toast disponíveis"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Toast:
    """Representa uma notificação toast"""

    def __init__(
        self,
        message: str,
        toast_type: str = ToastType.INFO,
        title: Optional[str] = None,
        duration: int = 5000
    ):
        self.message = message
        self.type = toast_type
        self.title = title or self._get_default_title(toast_type)
        self.duration = duration

    @staticmethod
    def _get_default_title(toast_type: str) -> str:
        """Retorna título padrão baseado no tipo"""
        titles = {
            ToastType.SUCCESS: "Sucesso",
            ToastType.ERROR: "Erro",
            ToastType.WARNING: "Atenção",
            ToastType.INFO: "Informação"
        }
        return titles.get(toast_type, "Notificação")

    def to_dict(self) -> Dict:
        """Converte toast para dicionário"""
        return {
            "message": self.message,
            "type": self.type,
            "title": self.title,
            "duration": self.duration
        }


def add_toast(
    request: Request,
    message: str,
    toast_type: str = ToastType.INFO,
    title: Optional[str] = None,
    duration: int = 5000
) -> None:
    """
    Adiciona uma notificação toast à sessão

    Args:
        request: Objeto Request do FastAPI
        message: Mensagem a ser exibida
        toast_type: Tipo do toast (success, error, warning, info)
        title: Título do toast (opcional)
        duration: Duração em milissegundos (padrão: 5000)

    Exemplo:
        add_toast(request, "Categoria criada com sucesso!", ToastType.SUCCESS)
    """
    if '_toasts' not in request.session:
        request.session['_toasts'] = []

    toast = Toast(message, toast_type, title, duration)
    request.session['_toasts'].append(toast.to_dict())


def toast_sucesso(
    request: Request,
    message: str,
    title: Optional[str] = None,
    duration: int = 5000
) -> None:
    """Adiciona toast de sucesso"""
    add_toast(request, message, ToastType.SUCCESS, title, duration)


def toast_erro(
    request: Request,
    message: str,
    title: Optional[str] = None,
    duration: int = 5000
) -> None:
    """Adiciona toast de erro"""
    add_toast(request, message, ToastType.ERROR, title, duration)


def toast_aviso(
    request: Request,
    message: str,
    title: Optional[str] = None,
    duration: int = 5000
) -> None:
    """Adiciona toast de aviso"""
    add_toast(request, message, ToastType.WARNING, title, duration)


def toast_info(
    request: Request,
    message: str,
    title: Optional[str] = None,
    duration: int = 5000
) -> None:
    """Adiciona toast de informação"""
    add_toast(request, message, ToastType.INFO, title, duration)


def toast_validacao_erro(
    request: Request,
    errors: List[str],
    title: str = "Erro de Validação"
) -> None:
    """
    Adiciona toast com erros de validação de formulário

    Args:
        request: Objeto Request do FastAPI
        errors: Lista de mensagens de erro
        title: Título do toast

    Exemplo:
        toast_validacao_erro(request, ["Nome é obrigatório", "Email inválido"])
    """
    if len(errors) == 1:
        message = errors[0]
    else:
        message = "<ul class='mb-0 ps-3'>" + "".join([f"<li>{erro}</li>" for erro in errors]) + "</ul>"

    add_toast(request, message, ToastType.ERROR, title, 7000)


def get_toasts(request: Request) -> List[Dict]:
    """
    Recupera e limpa os toasts da sessão

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Lista de dicionários representando os toasts
    """
    toasts = request.session.get('_toasts', [])
    if toasts:
        request.session['_toasts'] = []
    return toasts


def has_toasts(request: Request) -> bool:
    """Verifica se existem toasts pendentes"""
    return bool(request.session.get('_toasts', []))
