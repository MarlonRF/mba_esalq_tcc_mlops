"""
Conversao de colunas para inteiro.
"""
from typing import Iterable
import pandas as pd


def converter_colunas_int(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """Converte colunas para inteiro nullable (Int64), ignorando ausentes."""
    if not colunas:
        return df
    df = df.copy()
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    return df
