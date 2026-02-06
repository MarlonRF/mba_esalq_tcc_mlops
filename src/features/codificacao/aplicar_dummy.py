"""
One-hot encoding.
"""
from typing import Iterable
import pandas as pd


def aplicar_dummy(
    df: pd.DataFrame,
    colunas: Iterable[str],
    dropar_primeiro: bool = False,
    drop_first: bool = None,
    prefixo: str = None,
    prefixo_sep: str = "_",
) -> pd.DataFrame:
    """Aplica one-hot encoding com get_dummies."""
    # Compatibilidade: aceita drop_first ou dropar_primeiro
    if drop_first is not None:
        dropar_primeiro = drop_first
    
    cols = [c for c in colunas if c in df.columns]
    if not cols:
        return df
    
    # Usa prefixo se fornecido, senão usa o nome da coluna
    prefix = prefixo if prefixo is not None else cols
    
    return pd.get_dummies(df, columns=cols, drop_first=dropar_primeiro, prefix=prefix, prefix_sep=prefixo_sep)
