"""
Codificacao categorica (label ou one-hot) e mapeamentos.
"""
from .aplicar_codificacao_rotulos import aplicar_codificacao_rotulos
from .aplicar_dummy import aplicar_dummy

__all__ = [
    "aplicar_codificacao_rotulos",
    "aplicar_dummy",
]
