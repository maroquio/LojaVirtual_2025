# usuario_dto.py
from pydantic import EmailStr, Field, field_validator
from typing import Optional

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_numero_inteiro,
    validar_senha
)


class CriarUsuarioDTO(BaseDTO):
    """
    DTO para criação de novo usuário administrador.
    Usado em formulários de cadastro de admins.
    """
    nome: str = Field(..., description="Nome do Usuário")
    email: EmailStr = Field(..., description="Email do Usuário")
    senha: str = Field(..., min_length=6, description="Senha do Usuário")

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome", min_chars=2, max_chars=200)
        return valor

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=True)
        return valor


class AlterarUsuarioDTO(BaseDTO):
    """
    DTO para alteração de usuário administrador existente.
    Senha é opcional - se não fornecida, mantém a senha atual.
    """
    id: int = Field(..., ge=1, description="ID do Usuário")
    nome: str = Field(..., description="Nome do Usuário")
    email: EmailStr = Field(..., description="Email do Usuário")
    senha: Optional[str] = Field(None, min_length=6, description="Nova Senha (opcional)")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Usuário", obrigatorio=True, min_valor=1)
        return valor

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome", min_chars=2, max_chars=200)
        return valor

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        if valor is not None and valor.strip():
            validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=False)
        return valor


class ExcluirUsuarioDTO(BaseDTO):
    """
    DTO para exclusão de usuário administrador.
    """
    id: int = Field(..., ge=1, description="ID do Usuário")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Usuário", obrigatorio=True, min_valor=1)
        return valor
