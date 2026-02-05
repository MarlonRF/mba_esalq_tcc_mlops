"""Submódulo com funções de treinamento e otimização."""
# Importa versões unificadas (sobrescreve as legadas)
from .treinar_modelo_base_unified import treinar_modelo_base
from .otimizar_modelo_unified import otimizar_modelo
from .finalizar_modelo_unified import finalizar_modelo

__all__ = [
    "treinar_modelo_base",
    "otimizar_modelo",
    "finalizar_modelo",
]
