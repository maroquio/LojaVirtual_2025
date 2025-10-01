# auth_dto.py
from pydantic import EmailStr, Field, field_validator, ValidationInfo

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_cpf,
    validar_telefone,
    validar_senha,
    validar_senhas_coincidem
)


class LoginDTO(BaseDTO):
    """
    DTO para login de usuários.
    """
    email: EmailStr = Field(..., description="Email do Usuário")
    senha: str = Field(..., min_length=1, description="Senha do Usuário")

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        if not valor or not valor.strip():
            raise ValueError("Senha é obrigatória")
        return valor


class CadastroPublicoDTO(BaseDTO):
    """
    DTO para cadastro público de clientes.
    Usado no formulário de registro de novos clientes.
    """
    nome: str = Field(..., description="Nome Completo")
    email: EmailStr = Field(..., description="Email")
    cpf: str = Field(..., description="CPF")
    telefone: str = Field(..., description="Telefone")
    senha: str = Field(..., min_length=6, description="Senha")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação de Senha")

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

    @field_validator("confirmar_senha")
    def validar_confirmacao_senha(cls, valor, info: ValidationInfo):
        if 'senha' in info.data:
            validar_senhas_coincidem(info.data['senha'], valor)
        return valor


class EsqueciSenhaDTO(BaseDTO):
    """
    DTO para solicitação de redefinição de senha.
    """
    email: EmailStr = Field(..., description="Email cadastrado")


class RedefinirSenhaDTO(BaseDTO):
    """
    DTO para redefinição de senha via token.
    """
    senha: str = Field(..., min_length=6, description="Nova Senha")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação da Nova Senha")

    @field_validator("senha")
    def validar_senha_campo(cls, valor):
        validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=True)
        return valor

    @field_validator("confirmar_senha")
    def validar_confirmacao_senha(cls, valor, info: ValidationInfo):
        if 'senha' in info.data:
            validar_senhas_coincidem(info.data['senha'], valor)
        return valor
