"""
One-hot encoding.
"""
from typing import Iterable
import pandas as pd


def aplicar_one_hot(
    df: pd.DataFrame,
    colunas: Iterable[str],
    drop_first: bool = False,
    prefix_sep: str = "_",
) -> pd.DataFrame:
    """Aplica one-hot encoding com get_dummies."""
    cols = [c for c in colunas if c in df.columns]
    if not cols:
        return df
    return pd.get_dummies(df, columns=cols, drop_first=drop_first, prefix_sep=prefix_sep)
