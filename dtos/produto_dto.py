# produto_dto.py
from decimal import Decimal
from pydantic import Field, field_validator
from typing import Optional

from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_valor_monetario,
    validar_numero_inteiro
)


class CriarProdutoDTO(BaseDTO):
    """
    DTO para criação de novo produto.
    Usado em formulários de cadastro de produtos.
    """
    nome: str = Field(..., description="Nome do Produto")
    descricao: str = Field(..., description="Descrição do Produto")
    preco: float = Field(..., gt=0, description="Preço do Produto")
    quantidade: int = Field(..., ge=0, description="Quantidade em Estoque")
    categoria_id: int = Field(..., ge=1, description="ID da Categoria")

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome do Produto", min_chars=3, max_chars=200)
        return valor

    @field_validator("descricao")
    def validar_descricao(cls, valor):
        validar_texto_obrigatorio(valor, "Descrição do Produto", min_chars=10, max_chars=5000)
        return valor

    @field_validator("preco")
    def validar_preco(cls, valor):
        valor_decimal = Decimal(str(valor))
        validar_valor_monetario(valor_decimal, "Preço", obrigatorio=True, min_valor=Decimal('0.01'))
        return valor

    @field_validator("quantidade")
    def validar_quantidade(cls, valor):
        validar_numero_inteiro(valor, "Quantidade", obrigatorio=True, min_valor=0, max_valor=999999)
        return valor

    @field_validator("categoria_id")
    def validar_categoria_id(cls, valor):
        validar_numero_inteiro(valor, "ID da Categoria", obrigatorio=True, min_valor=1)
        return valor


class AlterarProdutoDTO(BaseDTO):
    """
    DTO para alteração de produto existente.
    """
    id: int = Field(..., ge=1, description="ID do Produto")
    nome: str = Field(..., description="Nome do Produto")
    descricao: str = Field(..., description="Descrição do Produto")
    preco: float = Field(..., gt=0, description="Preço do Produto")
    quantidade: int = Field(..., ge=0, description="Quantidade em Estoque")
    categoria_id: int = Field(..., ge=1, description="ID da Categoria")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Produto", obrigatorio=True, min_valor=1)
        return valor

    @field_validator("nome")
    def validar_nome(cls, valor):
        validar_texto_obrigatorio(valor, "Nome do Produto", min_chars=3, max_chars=200)
        return valor

    @field_validator("descricao")
    def validar_descricao(cls, valor):
        validar_texto_obrigatorio(valor, "Descrição do Produto", min_chars=10, max_chars=5000)
        return valor

    @field_validator("preco")
    def validar_preco(cls, valor):
        valor_decimal = Decimal(str(valor))
        validar_valor_monetario(valor_decimal, "Preço", obrigatorio=True, min_valor=Decimal('0.01'))
        return valor

    @field_validator("quantidade")
    def validar_quantidade(cls, valor):
        validar_numero_inteiro(valor, "Quantidade", obrigatorio=True, min_valor=0, max_valor=999999)
        return valor

    @field_validator("categoria_id")
    def validar_categoria_id(cls, valor):
        validar_numero_inteiro(valor, "ID da Categoria", obrigatorio=True, min_valor=1)
        return valor


class ExcluirProdutoDTO(BaseDTO):
    """
    DTO para exclusão de produto.
    """
    id: int = Field(..., ge=1, description="ID do Produto")

    @field_validator("id")
    def validar_id(cls, valor):
        validar_numero_inteiro(valor, "ID do Produto", obrigatorio=True, min_valor=1)
        return valor


class ReordenarFotosDTO(BaseDTO):
    """
    DTO para reordenação de fotos do produto.
    Recebe uma string com números separados por vírgula.
    """
    nova_ordem: str = Field(..., description="Nova ordem das fotos (números separados por vírgula)")

    @field_validator("nova_ordem")
    def validar_nova_ordem(cls, valor):
        if not valor or not valor.strip():
            raise ValueError("Nova ordem é obrigatória")

        try:
            # Tentar converter para lista de inteiros
            numeros = [int(x.strip()) for x in valor.split(",")]

            # Validar que todos são números positivos
            if any(n <= 0 for n in numeros):
                raise ValueError("Todos os números devem ser maiores que zero")

            # Validar que não há duplicatas
            if len(numeros) != len(set(numeros)):
                raise ValueError("Não pode haver números duplicados na ordem")

        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Nova ordem deve conter apenas números separados por vírgula")
            raise

        return valor
