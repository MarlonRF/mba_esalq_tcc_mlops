"""
Resolve nomes de colunas configuradas para os nomes reais existentes no DataFrame.
"""
from typing import List
import pandas as pd


def resolver_nomes_colunas_locais(
    dataframe_objeto: pd.DataFrame, nomes_colunas_configuradas: List[str]
) -> List[str]:
    """
    Resolve nomes de colunas configuradas para os nomes reais existentes no DataFrame.

    Faz correspondência entre nomes de colunas configurados e os nomes reais
    no DataFrame, considerando variações de capitalização e separadores.

    Args:
        dataframe_objeto (pd.DataFrame): DataFrame contendo as colunas a serem analisadas
        nomes_colunas_configuradas (List[str]): Lista de nomes de colunas a serem resolvidos

    Returns:
        List[str]: Lista com nomes reais das colunas encontradas no DataFrame
    """
    # Cria mapeamento de nomes em minúsculas para nomes originais
    mapeamento_minusculas = {
        nome_coluna.lower(): nome_coluna for nome_coluna in dataframe_objeto.columns
    }
    colunas_encontradas = []

    # Processa cada nome de coluna configurado
    for nome_coluna_config in nomes_colunas_configuradas or []:

        # 1. Verifica correspondência exata
        if nome_coluna_config in dataframe_objeto.columns:
            colunas_encontradas.append(nome_coluna_config)
            continue

        # 2. Verifica correspondência insensível a maiúsculas
        chave_minuscula = nome_coluna_config.lower()
        if chave_minuscula in mapeamento_minusculas:
            colunas_encontradas.append(mapeamento_minusculas[chave_minuscula])
            continue

        # 3. Verifica correspondência com normalização de separadores (_ <-> -)
        chave_alternativa = chave_minuscula.replace("_", "-").replace("-", "_")
        if chave_alternativa in mapeamento_minusculas:
            colunas_encontradas.append(mapeamento_minusculas[chave_alternativa])
            continue

    return colunas_encontradas


def resolver_nomes_colunas(
    dataframe_objeto: pd.DataFrame, nomes_colunas_configuradas: List[str]
) -> List[str]:
    """
    Versão genérica de resolução de colunas.

    Função wrapper que chama a resolução local de nomes de colunas.
    Mantida para compatibilidade com código existente.

    Args:
        dataframe_objeto (pd.DataFrame): DataFrame contendo as colunas a serem analisadas
        nomes_colunas_configuradas (List[str]): Lista de nomes de colunas a serem resolvidos

    Returns:
        List[str]: Lista com nomes reais das colunas encontradas no DataFrame
    """
    return resolver_nomes_colunas_locais(dataframe_objeto, nomes_colunas_configuradas)
