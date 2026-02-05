"""
Imputacao de valores faltantes numericos.
"""
import numpy as np
import pandas as pd


def imputar_numericos(df: pd.DataFrame, metodo: str = "median") -> pd.DataFrame:
    """Imputa numericos com mean/median/zero (aplica em todas colunas numericas)."""
    if metodo not in {"mean", "median", "zero"}:
        return df
    df = df.copy()
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns]
    for c in num_cols:
        if metodo == "mean":
            df[c] = df[c].fillna(df[c].mean())
        elif metodo == "median":
            df[c] = df[c].fillna(df[c].median())
        else:
            df[c] = df[c].fillna(0)
    return df
