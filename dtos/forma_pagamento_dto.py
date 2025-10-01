# forma_pagamento_dto.py
from pydantic import Field, field_validator

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_numero_inteiro
)


class CriarFormaPagamentoDTO(BaseDTO):
    """
    DTO para criação de nova forma de pagamento.
    """
    nome: str = Field(..., description="Nome da Forma de Pagamento")
    desconto: float = Field(..., ge=0, le=100, description="Desconto em percentual (0-100)")

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome da Forma de Pagamento", min_chars=2, max_chars=100)
        return valor

    @field_validator("desconto")
    def validar_desconto(cls, valor):
        if valor < 0 or valor > 100:
            raise ValueError("Desconto deve estar entre 0 e 100")
        return valor


class AlterarFormaPagamentoDTO(BaseDTO):
    """
    DTO para alteração de forma de pagamento existente.
    """
    id: int = Field(..., ge=1, description="ID da Forma de Pagamento")
    nome: str = Field(..., description="Nome da Forma de Pagamento")
    desconto: float = Field(..., ge=0, le=100, description="Desconto em percentual (0-100)")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID da Forma de Pagamento", obrigatorio=True, min_valor=1)
        return valor

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome da Forma de Pagamento", min_chars=2, max_chars=100)
        return valor

    @field_validator("desconto")
    def validar_desconto(cls, valor):
        if valor < 0 or valor > 100:
            raise ValueError("Desconto deve estar entre 0 e 100")
        return valor


class ExcluirFormaPagamentoDTO(BaseDTO):
    """
    DTO para exclusão de forma de pagamento.
    """
    id: int = Field(..., ge=1, description="ID da Forma de Pagamento")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID da Forma de Pagamento", obrigatorio=True, min_valor=1)
        return valor
