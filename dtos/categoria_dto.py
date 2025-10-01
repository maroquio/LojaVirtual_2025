# categoria_dto.py
from pydantic import Field, field_validator

from dtos.base_dto import BaseDTO
from util.validacoes_dto import validar_numero_inteiro, validar_texto_obrigatorio

class CriarCategoriaDTO(BaseDTO):
    nome: str = Field(..., description="Nome da Categoria")
    
    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome da Categoria", 8, 32)
        return valor
    

class AlterarCategoriaDTO(BaseDTO):
    id: int = Field(ge=1, description="ID da Categoria")
    nome: str = Field(..., description="Nome da Categoria")
    
    @field_validator("id")
    def validar_id(cls, valor):
        # if valor < 1:
        #     raise ValueError(f"ID da Categoria deve ser maior ou igual a 1, e você forneceu: {valor}.")
        validar_numero_inteiro("ID da Categoria", valor, True, 1)
        return valor

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome da Categoria")
        return valor