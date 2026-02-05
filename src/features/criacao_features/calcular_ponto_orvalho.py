"""
Calculo do ponto de orvalho.
"""
import numpy as np
import pandas as pd


def calcular_ponto_orvalho(temperatura_c: float, umidade_relativa: float) -> float:
    if pd.isna(temperatura_c) or pd.isna(umidade_relativa):
        return np.nan
    return temperatura_c - ((100.0 - umidade_relativa) / 5.0)
