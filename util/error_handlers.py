"""
Decoradores e handlers para tratamento de erros
"""

import functools
from typing import Callable, Optional
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from util.exceptions import ValidacaoError, RecursoNaoEncontradoError, LojaVirtualError
from util.flash_messages import informar_erro, informar_sucesso


def tratar_erro_rota(template_erro: Optional[str] = None,
                     redirect_erro: Optional[str] = None):
    """
    Decorador para tratar erros em rotas web

    Args:
        template_erro: Template para renderizar em caso de erro
        redirect_erro: URL para redirecionar em caso de erro

    Uso:
        @router.post("/cadastro")
        @tratar_erro_rota(template_erro="publico/cadastro.html")
        async def cadastrar(request: Request):
            # Seu código aqui
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                return await func(request, *args, **kwargs)

            except ValidationError as e:
                # Extrair primeira mensagem de erro do Pydantic
                error_msg = e.errors()[0]["msg"]
                # logger.warning("Erro de validação Pydantic", erro=error_msg, rota=str(request.url))

                if template_erro:
                    templates = Jinja2Templates(directory="templates")
                    return templates.TemplateResponse(template_erro, {
                        "request": request,
                        "erro": error_msg
                    })

            except ValidacaoError as e:
                # logger.warning("Erro de validação customizado", erro=e, rota=str(request.url))
                informar_erro(request, f"Dados inválidos: {e.mensagem}")

                if template_erro:
                    templates = Jinja2Templates(directory="templates")
                    return templates.TemplateResponse(template_erro, {
                        "request": request,
                        "erro": e.mensagem
                    })

            except RecursoNaoEncontradoError as e:
                # logger.info("Recurso não encontrado", erro=e, rota=str(request.url))
                informar_erro(request, e.mensagem)

            except LojaVirtualError as e:
                # logger.error("Erro de negócio", erro=e, rota=str(request.url))
                informar_erro(request, e.mensagem)

            except Exception as e:
                # logger.error("Erro inesperado", erro=e, rota=str(request.url))
                informar_erro(request, "Erro interno. Tente novamente.")

            # Fallback para redirect ou template
            if redirect_erro:
                from fastapi.responses import RedirectResponse
                return RedirectResponse(redirect_erro)
            elif template_erro:
                templates = Jinja2Templates(directory="templates")
                return templates.TemplateResponse(template_erro, {
                    "request": request,
                    "erro": "Ocorreu um erro. Tente novamente."
                })

        return wrapper
    return decorator