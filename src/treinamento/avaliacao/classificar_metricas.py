"""
Classifica modelos baseado em múltiplas métricas.
"""
from typing import List
import pandas as pd


def classificar_metricas(tabela: pd.DataFrame, metricas: List[str]) -> pd.DataFrame:
    """
    Classifica modelos baseado em múltiplas métricas e calcula uma classificação média.

    Args:
        tabela (pd.DataFrame): DataFrame contendo as métricas dos modelos
        metricas (List[str]): Lista das métricas a serem utilizadas para classificação

    Returns:
        pd.DataFrame: Tabela com colunas adicionais de classificação para cada métrica
                     e uma coluna de classificação média
                     
    Raises:
        ValueError: Se alguma métrica não existir na tabela
        
    Examples:
        >>> metricas = ['Accuracy', 'F1', 'Precision']
        >>> resultado = classificar_metricas(tabela_comparacao, metricas)
        >>> melhor_modelo = resultado.iloc[0]  # Modelo com melhor classificação média
    """
    # Valida se todas as métricas existem na tabela
    metricas_faltantes = [m for m in metricas if m not in tabela.columns]
    if metricas_faltantes:
        raise ValueError(f"Métricas não encontradas na tabela: {metricas_faltantes}")
    
    tabela_resultado = tabela.copy()
    
    # Cria coluna de classificação para cada métrica
    for metrica in metricas:
        tabela_resultado[f"classificacao_{metrica}"] = (
            tabela_resultado[metrica].rank(ascending=False, method="min").astype(int)
        )

    # Calcula classificação média
    tabela_resultado["classificacao_media"] = tabela_resultado[
        [f"classificacao_{m}" for m in metricas]
    ].mean(axis=1)

    # Ordena pela classificação média (melhor primeiro)
    tabela_resultado = tabela_resultado.sort_values("classificacao_media")

    return tabela_resultado
