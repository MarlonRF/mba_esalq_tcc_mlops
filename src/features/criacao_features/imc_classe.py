"""
Classificacao de IMC.
"""
import numpy as np
import pandas as pd


def imc_classe(v: float) -> str:
    if pd.isna(v):
        return np.nan
    if v < 18.5:
        return "Abaixo do peso"
    if v < 25:
        return "Peso Normal"
    if v < 30:
        return "Sobrepeso"
    if v < 35:
        return "Obesidade"
    if v < 40:
        return "Obesidade"
    return "Obesidade"
