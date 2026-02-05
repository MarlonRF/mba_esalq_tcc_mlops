"""
Normalizacao de colunas numericas.
"""
from typing import Dict, Iterable, Optional, Union
import pandas as pd
from .definir_escalar import pick_scaler


def normalizar(
    df: pd.DataFrame,
    colunas: Optional[Union[Iterable[str], Dict[str, str]]] = None,
    metodo: str = "standard",
    agrupamento: Optional[str] = None,
    sufixo: str = "_norm",
) -> pd.DataFrame:
    """
    Normaliza colunas numericas; se agrupamento for informado, aplica por grupo.
    
    Args:
        df: DataFrame a normalizar
        colunas: Colunas para normalizar. Pode ser:
            - None: normaliza todas colunas numéricas
            - Lista[str]: normaliza as colunas listadas com o mesmo método
            - Dict[str, str]: normaliza cada coluna com método específico
        metodo: Método padrão de normalização ('standard', 'minmax', 'robust')
        agrupamento: Coluna para agrupar antes de normalizar
        sufixo: Sufixo para colunas normalizadas
        
    Returns:
        DataFrame com colunas normalizadas adicionadas
    """
    df = df.copy()
    
    # Se colunas é um dicionário, aplicar normalização por coluna
    if isinstance(colunas, dict):
        for col, metodo_col in colunas.items():
            if col not in df.columns:
                continue
            df = _normalizar_coluna(df, col, metodo_col, agrupamento, sufixo)
        return df
    
    # Caso contrário, usar comportamento original
    cols = colunas or [c for c in df.select_dtypes(include=["number"]).columns]
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return df

    def _fit_transform(subdf: pd.DataFrame) -> pd.DataFrame:
        scaler = pick_scaler(metodo)
        valores = subdf[cols].values
        transformados = scaler.fit_transform(valores)
        for i, col in enumerate(cols):
            subdf[col + sufixo] = transformados[:, i]
        return subdf

    if agrupamento and agrupamento in df.columns:
        df = df.groupby(agrupamento, group_keys=False).apply(_fit_transform)
    else:
        df = _fit_transform(df)
    return df


def _normalizar_coluna(
    df: pd.DataFrame,
    coluna: str,
    metodo: str,
    agrupamento: Optional[str] = None,
    sufixo: str = "_norm",
) -> pd.DataFrame:
    """Normaliza uma única coluna com método específico."""
    def _fit_transform_col(subdf: pd.DataFrame) -> pd.DataFrame:
        scaler = pick_scaler(metodo)
        valores = subdf[[coluna]].values
        transformados = scaler.fit_transform(valores)
        subdf[coluna + sufixo] = transformados[:, 0]
        return subdf

    if agrupamento and agrupamento in df.columns:
        df = df.groupby(agrupamento, group_keys=False).apply(_fit_transform_col)
    else:
        df = _fit_transform_col(df)
    return df
