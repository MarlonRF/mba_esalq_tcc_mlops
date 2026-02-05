"""
One-hot encoding.
"""
from typing import Iterable
import pandas as pd


def aplicar_dummy(
    df: pd.DataFrame,
    colunas: Iterable[str],
    dropar_primeiro: bool = False,
    prefixo_sep: str = "_",
) -> pd.DataFrame:
    """Aplica one-hot encoding com get_dummies."""
    cols = [c for c in colunas if c in df.columns]
    if not cols:
        return df
    return pd.get_dummies(df, columns=cols, drop_first=dropar_primeiro, prefix_sep=prefixo_sep)
