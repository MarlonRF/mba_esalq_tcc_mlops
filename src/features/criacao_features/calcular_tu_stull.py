"""
Calculo da temperatura de bulbo umido (Stull 2011).
"""
import numpy as np
import pandas as pd


def calcular_tu_stull(temperatura: float, umidade_relativa: float) -> float:
    """Temperatura de bulbo umido (Stull 2011)."""
    if pd.isna(temperatura) or pd.isna(umidade_relativa):
        return np.nan
    return (
        temperatura * np.arctan(0.151977 * np.sqrt(umidade_relativa + 8.313659))
        + np.arctan(temperatura + umidade_relativa)
        - np.arctan(umidade_relativa - 1.676331)
        + 0.00391838 * (umidade_relativa ** 1.5) * np.arctan(0.023101 * umidade_relativa)
        - 4.686035
    )
