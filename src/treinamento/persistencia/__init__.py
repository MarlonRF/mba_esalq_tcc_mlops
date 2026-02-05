"""Submódulo de persistência de modelos."""
from .carregar_modelo import carregar_modelo
from .salvar_modelo import salvar_modelo

__all__ = [
    "carregar_modelo",
    "salvar_modelo",
]
