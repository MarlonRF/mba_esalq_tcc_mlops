"""
Conversao de colunas temporais.
"""
import pandas as pd


def converter_colunas_temporais(df: pd.DataFrame, coluna_data: str = "data", coluna_hora: str = "hora") -> pd.DataFrame:
    """Converte colunas de data/hora se existirem (formato brasileiro dia-first)."""
    df = df.copy()
    if coluna_data in df.columns:
        df[coluna_data] = pd.to_datetime(df[coluna_data], errors="coerce", dayfirst=True)
    if coluna_hora in df.columns:
        df[coluna_hora] = pd.to_datetime(
            df[coluna_hora], errors="coerce", format="%H:%M:%S"
        ).dt.time.fillna(
            pd.to_datetime(df[coluna_hora], errors="coerce", format="%H:%M").dt.time
        )
    return df
