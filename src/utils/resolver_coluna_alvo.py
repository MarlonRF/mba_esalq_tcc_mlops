"""
Resolve o nome final da coluna alvo baseado na configuração.
"""
from typing import Optional
import pandas as pd


def resolver_coluna_alvo(
    dataframe_processado: pd.DataFrame, configuracao_alvo: str
) -> Optional[str]:
    """
    Resolve o nome final da coluna alvo baseado na configuração e colunas disponíveis.

    Busca a coluna target/alvo no DataFrame considerando diferentes variações
    de nomenclatura e capitalização.

    Args:
        dataframe_processado (pd.DataFrame): DataFrame após processamento inicial
        configuracao_alvo (str): Nome configurado para a coluna alvo

    Returns:
        Optional[str]: Nome real da coluna alvo no DataFrame, ou None se não encontrada
    """
    # Cria mapeamento de nomes em minúsculas para nomes originais
    mapeamento_colunas_minusculas = {
        nome_coluna.lower(): nome_coluna for nome_coluna in dataframe_processado.columns
    }
    coluna_alvo_encontrada = None

    # 1. Verifica correspondência exata do nome configurado
    if configuracao_alvo in dataframe_processado.columns:
        coluna_alvo_encontrada = configuracao_alvo

    # 2. Verifica correspondência insensível a maiúsculas
    elif (
        configuracao_alvo and configuracao_alvo.lower() in mapeamento_colunas_minusculas
    ):
        coluna_alvo_encontrada = mapeamento_colunas_minusculas[
            configuracao_alvo.lower()
        ]

    # 3. Verifica correspondência com variações de separadores
    else:
        chave_base = (configuracao_alvo or "").lower().strip()
        chaves_alternativas = {
            chave_base,
            chave_base.replace("_", "-"),
            chave_base.replace("-", "_"),
        }
        for chave in chaves_alternativas:
            if chave in mapeamento_colunas_minusculas:
                coluna_alvo_encontrada = mapeamento_colunas_minusculas[chave]
                break

    return coluna_alvo_encontrada
