"""
Normalizacao de colunas numericas.
"""
from typing import Any, Dict, Iterable, Optional, Union
import pandas as pd
from .definir_escalar import pick_scaler


def normalizar(
    df: pd.DataFrame,
    colunas: Optional[Union[Iterable[str], Dict[str, str]]] = None,
    metodo: str = "standard",
    agrupamento: Optional[str] = None,
    sufixo: str = "",
) -> tuple[pd.DataFrame, Any]:
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
        Tupla (DataFrame normalizado, scaler(s) usados)
    """
    df_norm = df.copy()

    def _coluna_saida(nome_coluna: str) -> str:
        return f"{nome_coluna}{sufixo}" if sufixo else nome_coluna

    def _fit_transform_bloco(
        bloco: pd.DataFrame,
        cols_bloco: list[str],
        metodo_bloco: str,
    ) -> tuple[pd.DataFrame, Any]:
        if metodo_bloco == "standard":
            transformado = pd.DataFrame(index=bloco.index)
            scaler_info: Dict[str, Dict[str, float]] = {}
            for col in cols_bloco:
                media = bloco[col].mean()
                desvio = bloco[col].std(ddof=1)
                if pd.isna(desvio) or desvio == 0:
                    transformado[col] = 0.0
                else:
                    transformado[col] = (bloco[col] - media) / desvio
                scaler_info[col] = {"mean": float(media), "std": float(desvio) if not pd.isna(desvio) else 0.0}
            if len(cols_bloco) == 1:
                return transformado, scaler_info[cols_bloco[0]]
            return transformado, scaler_info

        scaler = pick_scaler(metodo_bloco)
        transformado = pd.DataFrame(
            scaler.fit_transform(bloco[cols_bloco]),
            columns=cols_bloco,
            index=bloco.index,
        )
        return transformado, scaler

    if isinstance(colunas, dict):
        scalers_dict: Dict[Any, Any] = {} if (agrupamento and agrupamento in df_norm.columns) else {}
        for col, metodo_col in colunas.items():
            if col not in df_norm.columns:
                continue
            col_out = _coluna_saida(col)
            if agrupamento and agrupamento in df_norm.columns:
                for grupo, idx in df_norm.groupby(agrupamento).groups.items():
                    bloco = df_norm.loc[idx, [col]]
                    transformado, scaler_obj = _fit_transform_bloco(bloco, [col], metodo_col)
                    df_norm.loc[idx, col_out] = transformado[col]
                    scalers_dict.setdefault(grupo, {})[col] = scaler_obj
            else:
                transformado, scaler_obj = _fit_transform_bloco(df_norm[[col]], [col], metodo_col)
                df_norm[col_out] = transformado[col]
                scalers_dict[col] = scaler_obj
        return df_norm, scalers_dict

    cols = list(colunas) if colunas is not None else list(df_norm.select_dtypes(include=["number"]).columns)
    cols = [c for c in cols if c in df_norm.columns]
    if not cols:
        return df_norm, None

    if agrupamento and agrupamento in df_norm.columns:
        scalers_grupo: Dict[Any, Any] = {}
        for grupo, idx in df_norm.groupby(agrupamento).groups.items():
            bloco = df_norm.loc[idx, cols]
            transformado, scaler_obj = _fit_transform_bloco(bloco, cols, metodo)
            for col in cols:
                df_norm.loc[idx, _coluna_saida(col)] = transformado[col]
            scalers_grupo[grupo] = scaler_obj
        return df_norm, scalers_grupo

    transformado, scaler_obj = _fit_transform_bloco(df_norm[cols], cols, metodo)
    for col in cols:
        df_norm[_coluna_saida(col)] = transformado[col]
    return df_norm, scaler_obj
