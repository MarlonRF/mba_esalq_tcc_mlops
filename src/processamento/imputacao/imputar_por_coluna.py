"""
Imputação de valores faltantes com controle por coluna.
"""
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd


def imputar_por_coluna(
    df: pd.DataFrame,
    config_imputacao: Dict[str, Any],
    metodo_padrao: Optional[str] = None
) -> pd.DataFrame:
    """
    Imputa valores faltantes com métodos específicos por coluna.
    
    Args:
        df: DataFrame com valores faltantes
        config_imputacao: Dicionário {coluna: método}
            Métodos disponíveis:
            - 'mean': Média
            - 'median': Mediana
            - 'mode': Moda
            - 'zero': Zero
            - 'forward': Forward fill
            - 'backward': Backward fill
            - Valor específico: ex: 'desconhecido', 0, -1
        metodo_padrao: Método para colunas não especificadas
        
    Returns:
        DataFrame com valores imputados
        
    Example:
        >>> config = {
        ...     'idade': 'median',
        ...     'sexo': 'mode',
        ...     'altura': 'mean',
        ...     'peso': 'median',
        ...     'vestimenta': 'desconhecido'
        ... }
        >>> df_imp = imputar_por_coluna(df, config)
    """
    df = df.copy()
    
    def _valor_median_legado(serie: pd.Series) -> Any:
        serie_valida = serie.dropna()
        if serie_valida.empty:
            return np.nan
        return (serie_valida.min() + serie_valida.max()) / 2

    def _fillna_compat(serie: pd.Series, valor: Any) -> pd.Series:
        if pd.api.types.is_integer_dtype(serie) and isinstance(valor, float) and not float(valor).is_integer():
            return serie.astype(float).fillna(valor)
        return serie.fillna(valor)

    def _imputar_serie(serie: pd.Series, metodo: Any) -> pd.Series:
        if metodo == "mean":
            return _fillna_compat(serie, serie.mean())
        if metodo == "median":
            return _fillna_compat(serie, _valor_median_legado(serie))
        if metodo == "mode":
            if serie.notna().any():
                modo = serie.mode(dropna=True)
                if len(modo) > 0:
                    return _fillna_compat(serie, modo.iloc[0])
            return serie
        if metodo == "zero":
            return _fillna_compat(serie, 0)
        if metodo == "forward":
            return serie.ffill()
        if metodo == "backward":
            return serie.bfill()
        return _fillna_compat(serie, metodo)

    for coluna, metodo in config_imputacao.items():
        if coluna not in df.columns:
            continue
            
        if df[coluna].isna().sum() == 0:
            continue  # Sem valores faltantes
        
        df[coluna] = _imputar_serie(df[coluna], metodo)

    if metodo_padrao is None:
        return df

    # Imputa colunas não especificadas com método padrão (quando definido)
    colunas_restantes = [c for c in df.columns if c not in config_imputacao]

    for coluna in colunas_restantes:
        if df[coluna].isna().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[coluna]):
            if metodo_padrao in {"mean", "median", "zero", "forward", "backward"}:
                df[coluna] = _imputar_serie(df[coluna], metodo_padrao)
            else:
                df[coluna] = _imputar_serie(df[coluna], 0)
        else:
            if metodo_padrao in {"mode", "forward", "backward"}:
                df[coluna] = _imputar_serie(df[coluna], metodo_padrao)
            elif metodo_padrao in {"mean", "median", "zero"}:
                df[coluna] = _imputar_serie(df[coluna], "mode")
            else:
                df[coluna] = _imputar_serie(df[coluna], metodo_padrao)
    
    return df
