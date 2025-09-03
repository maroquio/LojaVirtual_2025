from typing import Any, Optional
from datetime import datetime
from model.usuario_model import Usuario
from sql.usuario_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return (cursor.rowcount > 0)

def inserir(usuario: Usuario, cursor: Any = None) -> Optional[int]:
    if cursor:
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.perfil))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.perfil))
            return cursor.lastrowid
    
def alterar(usuario: Usuario, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.id))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ALTERAR, (
                usuario.nome,
                usuario.email,
                usuario.id))
            return (cursor.rowcount > 0)
    
def atualizar_senha(id: int, senha: str, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(ALTERAR_SENHA, (senha, id))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ALTERAR_SENHA, (senha, id))
            return (cursor.rowcount > 0)
    
def excluir(id: int, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id,))
            return (cursor.rowcount > 0)
    
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"])
            return usuario
        return None

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"]) 
                for row in rows]
        return usuarios

def obter_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"])
            return usuario
        return None

def atualizar_token(email: str, token: str, data_expiracao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TOKEN, (token, data_expiracao, email))
        return (cursor.rowcount > 0)

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return (cursor.rowcount > 0)

def obter_por_token(token: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"])
            return usuario
        return None

def limpar_token(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET token_redefinicao=NULL, data_token=NULL WHERE id=?", (id,))
        return (cursor.rowcount > 0)

def obter_todos_por_perfil(perfil: str) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE perfil=? ORDER BY nome", (perfil,))
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuario = Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                data_cadastro=row["data_cadastro"]
            )
            usuarios.append(usuario)
        return usuarios