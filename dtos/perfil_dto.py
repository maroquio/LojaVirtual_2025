# perfil_dto.py
from pydantic import EmailStr, Field, field_validator, ValidationInfo
from typing import Optional

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_cpf,
    validar_telefone,
    validar_senha,
    validar_senhas_coincidem
)


class AtualizarPerfilDTO(BaseDTO):
    """
    DTO para atualização de dados do perfil do usuário.
    CPF e telefone são opcionais (apenas para clientes).
    """
    nome: str = Field(..., description="Nome do Usuário")
    email: EmailStr = Field(..., description="Email do Usuário")
    cpf: Optional[str] = Field(None, description="CPF (apenas para clientes)")
    telefone: Optional[str] = Field(None, description="Telefone (apenas para clientes)")

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome", min_chars=2, max_chars=200)
        return valor

    @field_validator("cpf")
    def validar_cpf_campo(cls, valor):
        if valor and valor.strip():
            return validar_cpf(valor)
        return valor

    @field_validator("telefone")
    def validar_telefone_campo(cls, valor):
        if valor and valor.strip():
            return validar_telefone(valor)
        return valor


class AlterarSenhaDTO(BaseDTO):
    """
    DTO para alteração de senha do usuário logado.
    Requer senha atual para validação.
    """
    senha_atual: str = Field(..., min_length=1, description="Senha Atual")
    senha_nova: str = Field(..., min_length=6, description="Nova Senha")
    confirmar_senha: str = Field(..., min_length=6, description="Confirmação da Nova Senha")

    @field_validator("senha_atual")
    def validar_senha_atual(cls, valor):
        if not valor or not valor.strip():
            raise ValueError("Senha atual é obrigatória")
        return valor

    @field_validator("senha_nova")
    def validar_senha_nova(cls, valor, info: ValidationInfo):
        validar_senha(valor, min_chars=6, max_chars=128, obrigatorio=True)

        # Verificar se a nova senha é diferente da atual
        if 'senha_atual' in info.data and valor == info.data['senha_atual']:
            raise ValueError("Nova senha deve ser diferente da senha atual")

        return valor

    @field_validator("confirmar_senha")
    def validar_confirmacao_senha(cls, valor, info: ValidationInfo):
        if 'senha_nova' in info.data:
            validar_senhas_coincidem(info.data['senha_nova'], valor)
        return valor
