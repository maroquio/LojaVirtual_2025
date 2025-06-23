CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cliente (
id INTEGER PRIMARY KEY,
cpf TEXT NOT NULL,
telefone TEXT NOT NULL,
FOREIGN KEY (id) REFERENCES usuario(id)
"""

INSERIR = """
INSERT INTO cliente (cpf, telefone) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE cliente
SET cpf=?, telefone=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM cliente
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
c.id, c.cpf, c.telefone, u.nome, u.email, u.senha
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
WHERE c.id=?
"""

OBTER_TODOS = """
SELECT 
c.id, c.cpf, c.telefone, u.nome, u.email, u.senha
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
ORDER BY u.nome
""" 