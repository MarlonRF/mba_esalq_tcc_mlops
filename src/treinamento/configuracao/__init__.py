"""Submódulo de configuração dos experimentos de treinamento."""
# Versões unificadas (recomendadas)
from .criar_experimento import criar_experimento

# Versões legadas (retrocompatibilidade)
from .criar_experimento_classificacao import criar_experimento_classificacao

from .configurar_parametros import (
    configurar_parametros,
    validar_parametros,
    parametros_rapidos,
)

__all__ = [
    "criar_experimento",  # Unificado
    "criar_experimento_classificacao",  # Legacy
    "configurar_parametros",
    "validar_parametros",
    "parametros_rapidos",
]
