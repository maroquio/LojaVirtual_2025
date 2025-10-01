"""
Middleware de Notificações Toast
Inspirado no sistema de flash messages do projeto CaseBem

Este middleware injeta as notificações toast no contexto dos templates.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from util.toast_messages import get_toasts


class ToastMiddleware(BaseHTTPMiddleware):
    """
    Middleware que adiciona toasts ao contexto de template
    """

    async def dispatch(self, request: Request, call_next):
        # Processar a requisição
        response = await call_next(request)

        # Não precisamos fazer nada aqui, pois os toasts são injetados
        # diretamente no contexto do template através do template_util
        return response


def inject_toasts(request: Request) -> dict:
    """
    Função auxiliar para injetar toasts no contexto do template

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Dicionário com os toasts para o template
    """
    return {
        "toasts": get_toasts(request)
    }
