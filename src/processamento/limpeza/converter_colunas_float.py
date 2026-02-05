"""
Conversao de colunas para float.
"""
from typing import Iterable
import pandas as pd


def _converter_para_float(serie: pd.Series) -> pd.Series:
    """Converte serie para float tratando virgulas decimais brasileiras."""
    tratada = serie.astype(str).str.replace(",", ".", regex=False)
    return pd.to_numeric(tratada, errors="coerce")


def converter_colunas_float(df: pd.DataFrame, colunas: Iterable[str]) -> pd.DataFrame:
    """Converte colunas para float tratando virgula decimal.

    Usa to_numeric com errors="coerce"; colunas ausentes sao ignoradas.
    """
    if not colunas:
        return df
    df = df.copy()
    for col in colunas:
        if col in df.columns:
            df[col] = _converter_para_float(df[col])
    return df
