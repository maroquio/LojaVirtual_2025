from .base_dto import BaseDTO
from .categoria_dto import CriarCategoriaDTO, AlterarCategoriaDTO
from .produto_dto import CriarProdutoDTO, AlterarProdutoDTO, ExcluirProdutoDTO, ReordenarFotosDTO
from .usuario_dto import CriarUsuarioDTO, AlterarUsuarioDTO, ExcluirUsuarioDTO
from .cliente_dto import CriarClienteDTO, AlterarClienteDTO, ExcluirClienteDTO
from .forma_pagamento_dto import CriarFormaPagamentoDTO, AlterarFormaPagamentoDTO, ExcluirFormaPagamentoDTO
from .auth_dto import LoginDTO, CadastroPublicoDTO, EsqueciSenhaDTO, RedefinirSenhaDTO
from .perfil_dto import AtualizarPerfilDTO, AlterarSenhaDTO


__all__ = [
    # Base
    'BaseDTO',

    # Categoria
    'CriarCategoriaDTO',
    'AlterarCategoriaDTO',

    # Produto
    'CriarProdutoDTO',
    'AlterarProdutoDTO',
    'ExcluirProdutoDTO',
    'ReordenarFotosDTO',

    # Usuário
    'CriarUsuarioDTO',
    'AlterarUsuarioDTO',
    'ExcluirUsuarioDTO',

    # Cliente
    'CriarClienteDTO',
    'AlterarClienteDTO',
    'ExcluirClienteDTO',

    # Forma de Pagamento
    'CriarFormaPagamentoDTO',
    'AlterarFormaPagamentoDTO',
    'ExcluirFormaPagamentoDTO',

    # Autenticação
    'LoginDTO',
    'CadastroPublicoDTO',
    'EsqueciSenhaDTO',
    'RedefinirSenhaDTO',

    # Perfil
    'AtualizarPerfilDTO',
    'AlterarSenhaDTO',
]