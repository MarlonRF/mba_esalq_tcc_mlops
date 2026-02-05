"""
Conversao de colunas para categoricas.
"""
from typing import Iterable
import pandas as pd


def converter_colunas_categoricas(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """Converte colunas para string/categorical leve."""
    if not colunas:
        return df
    df = df.copy()
    for col in colunas:
        if col in df.columns:
            df[col] = df[col].astype("string")
    return df
