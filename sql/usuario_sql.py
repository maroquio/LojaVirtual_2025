CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
senha TEXT NOT NULL,
perfil TEXT NOT NULL DEFAULT 'cliente',
foto TEXT,
token_redefinicao TEXT,
data_token TIMESTAMP
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, perfil)
VALUES (?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome=?, email=?
WHERE id=?
"""

ALTERAR_SENHA = """
UPDATE usuario
SET senha=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
id, nome, email, senha, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE id=?
"""

OBTER_TODOS = """
SELECT 
id, nome, email, senha, perfil, foto
FROM usuario
ORDER BY nome
"""

OBTER_POR_EMAIL = """
SELECT 
id, nome, email, senha, perfil, foto
FROM usuario
WHERE email=?
"""

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao=?, data_token=?
WHERE email=?
"""

ATUALIZAR_FOTO = """
UPDATE usuario
SET foto=?
WHERE id=?
"""

OBTER_POR_TOKEN = """
SELECT 
id, nome, email, senha, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE token_redefinicao=? AND data_token > datetime('now')
"""