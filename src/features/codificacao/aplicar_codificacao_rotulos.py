"""
Aplicacao de label encoding.
"""
from typing import Dict, Iterable, Tuple
import pandas as pd
from .codificar_label import codificar_label


def aplicar_codificacao_rotulos(
    df: pd.DataFrame,
    colunas: Iterable[str],
    sufixo: str = "_cod",
) -> Tuple[pd.DataFrame, Dict[str, Dict[int, str]]]:
    """Aplica label encoding nas colunas informadas."""
    if not colunas:
        return df, {}
    df = df.copy()
    mapa_rotulos = {}
    for col in colunas:
        if col in df.columns:
            codigos, mapa = codificar_label(df[col])
            df[f"{col}{sufixo}"] = codigos
            mapa_rotulos[col] = mapa
    return df, mapa_rotulos
