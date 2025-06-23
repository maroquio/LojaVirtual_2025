CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha)
VALUES (?, ?, ?)
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
id, nome, email, senha
FROM usuario
WHERE id=?
"""

OBTER_TODOS = """
SELECT 
id, nome, email, senha
FROM usuario
ORDER BY nome
"""