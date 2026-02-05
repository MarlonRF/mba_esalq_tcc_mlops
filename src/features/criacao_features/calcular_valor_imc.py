"""
Calculo de IMC.
"""
import numpy as np
import pandas as pd


def calcular_valor_imc(peso_kg: float, altura_cm: float) -> float:
    if pd.isna(peso_kg) or pd.isna(altura_cm) or altura_cm == 0:
        return np.nan
    altura_m = altura_cm / 100.0
    return peso_kg / (altura_m ** 2)
