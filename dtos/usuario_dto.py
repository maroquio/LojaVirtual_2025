from pydantic import BaseModel, field_validator


class CadastroUsuarioDTO(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: str
    senha: str
    confirmar_senha: str

    @field_validator('nome')
    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError('Nome é obrigatório.')
        if len(nome.split()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 palavras.')
        return nome
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, cpf):
        if not cpf:
            raise ValueError('CPF é obrigatório.')
        if len(cpf) != 11:
            raise ValueError('CPF deve ter 11 dígitos.')
        return cpf

    @field_validator('email')
    @classmethod
    def validate_email(cls, email):
        if not email:
            raise ValueError('E-mail é obrigatório.')
        if '@' not in email or '.' not in email:
            raise ValueError('E-mail inválido.')
        return email

    @field_validator('senha')
    @classmethod
    def validate_senha(cls, senha):
        if not senha:
            raise ValueError('Senha é obrigatória.')
        if len(senha) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres.')
        return senha