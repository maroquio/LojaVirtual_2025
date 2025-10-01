# cliente_dto.py
from pydantic import EmailStr, Field, field_validator
from typing import Optional

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_cpf,
    validar_telefone,
    validar_senha,
    validar_numero_inteiro
)


class CriarClienteDTO(BaseDTO):
    """
    DTO para criação de novo cliente.
    Usado em formulários de cadastro de clientes (admin).
    """
    nome: str = Field(..., description="Nome do Cliente")
    cpf: str = Field(..., description="CPF do Cliente")
    email: EmailStr = Field(..., description="Email do Cliente")
    telefone: str = Field(..., description="Telefone do Cliente")
    senha: str = Field(..., min_length=6, description="Senha do Cliente")

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome", min_chars=2, max_chars=200)
        return valor

    @field_validator("cpf")
    def validar_cpf_campo(cls, valor):
        cpf_limpo = validar_cpf(valor)
        if not cpf_limpo:
            raise ValueError("CPF é obrigatório")
        return cpf_limpo

    @field_validator("telefone")
    def validar_telefone_campo(cls, valor):
        return validar_telefone(valor)

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=True)
        return valor


class AlterarClienteDTO(BaseDTO):
    """
    DTO para alteração de cliente existente.
    Senha é opcional - se não fornecida, mantém a senha atual.
    """
    id: int = Field(..., ge=1, description="ID do Cliente")
    nome: str = Field(..., description="Nome do Cliente")
    cpf: str = Field(..., description="CPF do Cliente")
    email: EmailStr = Field(..., description="Email do Cliente")
    telefone: str = Field(..., description="Telefone do Cliente")
    senha: Optional[str] = Field(None, min_length=6, description="Nova Senha (opcional)")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Cliente", obrigatorio=True, min_valor=1)
        return valor

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome", min_chars=2, max_chars=200)
        return valor

    @field_validator("cpf")
    def validar_cpf_campo(cls, valor):
        cpf_limpo = validar_cpf(valor)
        if not cpf_limpo:
            raise ValueError("CPF é obrigatório")
        return cpf_limpo

    @field_validator("telefone")
    def validar_telefone_campo(cls, valor):
        return validar_telefone(valor)

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        if valor is not None and valor.strip():
            validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=False)
        return valor


class ExcluirClienteDTO(BaseDTO):
    """
    DTO para exclusão de cliente.
    """
    id: int = Field(..., ge=1, description="ID do Cliente")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Cliente", obrigatorio=True, min_valor=1)
        return valor
