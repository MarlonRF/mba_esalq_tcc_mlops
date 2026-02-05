"""
Calculo de heat index.
"""
import numpy as np
import pandas as pd


def calcular_heat_index(temperatura_c: float, umidade_relativa: float) -> float:
    if pd.isna(temperatura_c) or pd.isna(umidade_relativa):
        return np.nan
    return (
        -8.78469475556
        + 1.61139411 * temperatura_c
        + 2.33854883889 * umidade_relativa
        - 0.14611605 * temperatura_c * umidade_relativa
    )
