"""
Adicao de coluna mes-ano.
"""
import pandas as pd


def adicionar_mes_ano(df: pd.DataFrame, coluna_data: str = "data", nome_coluna: str = "mes-ano") -> pd.DataFrame:
    """Adiciona coluna mes-ano (MM-YYYY) se coluna de data existir."""
    if coluna_data not in df.columns:
        return df
    df = df.copy()
    dt = pd.to_datetime(df[coluna_data], errors="coerce")
    df[nome_coluna] = dt.dt.strftime("%m-%Y").fillna("desconhecido")
    return df
