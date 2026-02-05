"""
Aplicacao de substituicoes padrao.
"""
from typing import Dict
import pandas as pd


def aplicar_substituicoes(df: pd.DataFrame, substituicoes: Dict) -> pd.DataFrame:
    """Aplica substituicoes padrao (e.g., 'x' -> NaN) retornando copia."""
    if not substituicoes:
        return df
    return df.replace(substituicoes)
