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
    
    # Passo 1: Média móvel
    df[coluna] = df[coluna].fillna(
        df[coluna].rolling(window=window, min_periods=1).mean()
    )
    
    # Passo 2: Interpolação
    df[coluna] = df[coluna].interpolate(method=metodo_interpolacao)
    
    return df
