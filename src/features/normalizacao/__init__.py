"""
Normalização de dados numéricos.
"""
from .normalizar import normalizar
from .definir_escalar import pick_scaler, SCALERS

__all__ = [
    "normalizar",
    "pick_scaler",
    "SCALERS",
]
