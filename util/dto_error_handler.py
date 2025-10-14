"""
Utilitário para tratamento de erros de validação de DTOs
Converte erros do Pydantic em notificações toast
"""

from typing import List
from pydantic import ValidationError
from fastapi import Request
from util.toast_messages import toast_validacao_erro


def tratar_erro_validacao(request: Request, erro: ValidationError) -> List[str]:
    """
    Converte erros de validação do Pydantic em mensagens legíveis
    e adiciona um toast de erro

    Args:
        request: Objeto Request do FastAPI
        erro: Exceção de validação do Pydantic

    Returns:
        Lista de mensagens de erro formatadas
    """
    erros = []

    for erro_item in erro.errors():
        campo_raw = erro_item['loc'][-1] if erro_item['loc'] else 'campo'
        campo = str(campo_raw)  # Converter para string
        tipo = erro_item['type']
        mensagem = erro_item['msg']

        # Traduzir tipos de erro comuns para português
        if tipo == 'value_error':
            erro_formatado = mensagem
        elif tipo == 'missing':
            erro_formatado = f"{campo.replace('_', ' ').title()} é obrigatório"
        elif tipo == 'string_too_short':
            min_length = erro_item.get('ctx', {}).get('min_length', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ter no mínimo {min_length} caracteres"
        elif tipo == 'string_too_long':
            max_length = erro_item.get('ctx', {}).get('max_length', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ter no máximo {max_length} caracteres"
        elif tipo == 'value_error.email':
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ser um email válido"
        elif tipo == 'greater_than':
            limite = erro_item.get('ctx', {}).get('gt', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ser maior que {limite}"
        elif tipo == 'greater_than_equal':
            limite = erro_item.get('ctx', {}).get('ge', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ser maior ou igual a {limite}"
        elif tipo == 'less_than':
            limite = erro_item.get('ctx', {}).get('lt', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ser menor que {limite}"
        elif tipo == 'less_than_equal':
            limite = erro_item.get('ctx', {}).get('le', '')
            erro_formatado = f"{campo.replace('_', ' ').title()} deve ser menor ou igual a {limite}"
        else:
            # Para outros tipos, usar a mensagem padrão
            erro_formatado = f"{campo.replace('_', ' ').title()}: {mensagem}"

        erros.append(erro_formatado)

    # Adicionar toast com os erros
    toast_validacao_erro(request, erros)

    return erros


def dto_form_data(form_class, form_data: dict):
    """
    Cria uma instância de DTO a partir de dados de formulário,
    tratando erros de validação

    Args:
        form_class: Classe do DTO
        form_data: Dicionário com dados do formulário

    Returns:
        Instância do DTO ou None em caso de erro de validação

    Raises:
        ValidationError: Se houver erro de validação
    """
    try:
        return form_class(**form_data)
    except ValidationError as e:
        raise e
