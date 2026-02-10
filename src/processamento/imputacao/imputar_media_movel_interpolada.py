"""
Imputação com média móvel e interpolação (para séries temporais).
"""
import pandas as pd
from typing import Optional


def imputar_media_movel_interpolada(
    df: pd.DataFrame,
    coluna: str,
    window: int = 48,
    metodo_interpolacao: str = "linear"
) -> pd.DataFrame:
    """
    Imputa valores usando média móvel seguida de interpolação.
    
    Útil para séries temporais meteorológicas.
    
    Args:
        df: DataFrame
        coluna: Nome da coluna
        window: Tamanho da janela para média móvel
        metodo_interpolacao: Método de interpolação (linear, polynomial, etc)
        
    Returns:
        DataFrame com valores imputados
    """
    df = df.copy()
    
    if coluna not in df.columns:
        return df
    
    serie = df[coluna]
    if serie.isna().sum() == 0:
        return df
    if serie.notna().sum() == 0:
        return df

    # Interpola primeiro para respeitar continuidade temporal dos dados.
    serie_imputada = serie.interpolate(method=metodo_interpolacao, limit_direction="both")

    # Se restarem NaN (cenários específicos), usa média móvel como fallback.
    if serie_imputada.isna().any():
        media_movel = serie_imputada.rolling(window=window, min_periods=1).mean()
        serie_imputada = serie_imputada.fillna(media_movel)

    df[coluna] = serie_imputada
    return df
