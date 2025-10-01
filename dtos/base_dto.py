# base_dto.py
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any
from util.validacoes_dto import ValidacaoError


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        # Remover espaços em branco automaticamente
        str_strip_whitespace=True,
        # Validar na atribuição também (não só na criação)
        validate_assignment=True,
        # Usar valores dos enums ao invés dos objetos
        use_enum_values=True,
        # Permitir population by name (útil para formulários HTML)
        populate_by_name=True,
        # Validar valores padrão também
        validate_default=True
    )

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> Dict[str, Any]:
        return {"exemplo": "Sobrescrever na classe filha", **overrides}

    @classmethod
    def validar_campo_wrapper(cls, validador_func, campo_nome: str = ""):
        def wrapper(valor, **kwargs):
            try:
                if campo_nome:
                    return validador_func(valor, campo_nome, **kwargs)
                else:
                    return validador_func(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return wrapper

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __str__(self) -> str:
        campos = ', '.join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"{self.__class__.__name__}({campos})"

    def __repr__(self) -> str:
        return self.__str__()