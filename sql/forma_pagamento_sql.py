CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS forma_pagamento (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
desconto REAL NOT NULL)
"""

INSERIR = """
INSERT INTO forma_pagamento (nome, desconto)
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT
id, nome, desconto
FROM forma_pagamento
ORDER BY nome
"""