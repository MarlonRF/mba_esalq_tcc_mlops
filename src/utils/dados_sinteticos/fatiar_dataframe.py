"""
Fatia um DataFrame conforme índices ou slice desejado.
"""
from typing import List, Optional
import pandas as pd


def fatiar_dataframe(
    df: pd.DataFrame,
    inicio: Optional[int] = None,
    fim: Optional[int] = None,
    indices: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Fatia um DataFrame conforme índices ou slice desejado.

    Args:
        df (pd.DataFrame): DataFrame original.
        inicio (int, opcional): Índice inicial do slice.
        fim (int, opcional): Índice final do slice.
        indices (List[int], opcional): Lista de índices específicos.

    Returns:
        pd.DataFrame: DataFrame fatiado.
    """
    if indices is not None:
        return df.iloc[indices]
    else:
        return df.iloc[inicio:fim]
