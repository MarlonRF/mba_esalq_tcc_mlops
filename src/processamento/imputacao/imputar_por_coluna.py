"""
Imputação de valores faltantes com controle por coluna.
"""
from typing import Dict, Optional
import numpy as np
import pandas as pd


def imputar_por_coluna(
    df: pd.DataFrame,
    config_imputacao: Dict[str, str],
    metodo_padrao: str = "median"
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
    
    for coluna, metodo in config_imputacao.items():
        if coluna not in df.columns:
            continue
            
        if df[coluna].isna().sum() == 0:
            continue  # Sem valores faltantes
        
        # Aplicar método de imputação
        if metodo == 'mean':
            df[coluna] = df[coluna].fillna(df[coluna].mean())
        elif metodo == 'median':
            df[coluna] = df[coluna].fillna(df[coluna].median())
        elif metodo == 'mode':
            if df[coluna].notna().any():
                modo = df[coluna].mode(dropna=True)
                if len(modo) > 0:
                    df[coluna] = df[coluna].fillna(modo.iloc[0])
        elif metodo == 'zero':
            df[coluna] = df[coluna].fillna(0)
        elif metodo == 'forward':
            df[coluna] = df[coluna].fillna(method='ffill')
        elif metodo == 'backward':
            df[coluna] = df[coluna].fillna(method='bfill')
        else:
            # Valor constante específico
            df[coluna] = df[coluna].fillna(metodo)
    
    # Imputa colunas não especificadas com método padrão
    colunas_restantes = [c for c in df.columns if c not in config_imputacao]
    
    for coluna in colunas_restantes:
        if df[coluna].isna().sum() == 0:
            continue
        
        # Detecta tipo da coluna
        if pd.api.types.is_numeric_dtype(df[coluna]):
            if metodo_padrao == 'mean':
                df[coluna] = df[coluna].fillna(df[coluna].mean())
            elif metodo_padrao == 'median':
                df[coluna] = df[coluna].fillna(df[coluna].median())
            else:
                df[coluna] = df[coluna].fillna(0)
        else:
            # Categórica
            if df[coluna].notna().any():
                modo = df[coluna].mode(dropna=True)
                if len(modo) > 0:
                    df[coluna] = df[coluna].fillna(modo.iloc[0])
    
    return df
