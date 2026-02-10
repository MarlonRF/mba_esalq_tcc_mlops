"""
Calculo de heat index.
"""
import numpy as np
import pandas as pd


def calcular_heat_index(temperatura_c: float, umidade_relativa: float) -> float:
    if pd.isna(temperatura_c) or pd.isna(umidade_relativa):
        return np.nan
    temperatura_f = (temperatura_c * 9 / 5) + 32
    umidade = float(umidade_relativa)

    # Equação de Rothfusz (NOAA), em Fahrenheit.
    heat_index_f = (
        -42.379
        + 2.04901523 * temperatura_f
        + 10.14333127 * umidade
        - 0.22475541 * temperatura_f * umidade
        - 0.00683783 * (temperatura_f**2)
        - 0.05481717 * (umidade**2)
        + 0.00122874 * (temperatura_f**2) * umidade
        + 0.00085282 * temperatura_f * (umidade**2)
        - 0.00000199 * (temperatura_f**2) * (umidade**2)
    )

    return (heat_index_f - 32) * 5 / 9
