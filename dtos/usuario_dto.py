# usuario_dto.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_numero_inteiro,
    validar_senha
)


# DTOs para administração de usuários (área admin)
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


# DTOs para cadastro público de usuários (área pública)
class CadastroUsuarioDTO(BaseModel):
    """
    DTO para cadastro público de novos usuários/clientes.
    Usado no formulário de cadastro público da loja.
    """
    nome: str
    cpf: str
    telefone: str
    email: str
    senha: str
    confirmar_senha: str

    @field_validator('nome')
    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError('Nome é obrigatório.')
        if len(nome.split()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 palavras.')
        return nome

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, cpf):
        if not cpf:
            raise ValueError('CPF é obrigatório.')
        if len(cpf) != 11:
            raise ValueError('CPF deve ter 11 dígitos.')
        return cpf

    @field_validator('email')
    @classmethod
    def validate_email(cls, email):
        if not email:
            raise ValueError('E-mail é obrigatório.')
        if '@' not in email or '.' not in email:
            raise ValueError('E-mail inválido.')
        return email

    @field_validator('senha')
    @classmethod
    def validate_senha(cls, senha):
        if not senha:
            raise ValueError('Senha é obrigatória.')
        if len(senha) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres.')
        return senha

    @field_validator('confirmar_senha')
    @classmethod
    def validate_confirmar_senha(cls, confirmar_senha, values):
        senha = values.data.get('senha') if hasattr(values, 'data') else None
        if not confirmar_senha:
            raise ValueError('Confirmação de senha é obrigatória.')
        if senha and confirmar_senha != senha:
            raise ValueError('Senhas não coincidem.')
        return confirmar_senha
