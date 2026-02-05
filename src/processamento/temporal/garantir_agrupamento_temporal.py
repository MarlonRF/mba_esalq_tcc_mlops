"""
Garantia de agrupamento temporal.
"""
import pandas as pd
from .converter_colunas_temporais import converter_colunas_temporais
from .adicionar_mes_ano import adicionar_mes_ano


def garantir_agrupamento_temporal(df: pd.DataFrame, coluna_data: str = "data", coluna_hora: str = "hora", nome_coluna: str = "mes-ano") -> pd.DataFrame:
    """Garante coluna de agrupamento temporal (mes-ano) se nao existir."""
    if nome_coluna in df.columns or nome_coluna.replace("-", "_") in df.columns:
        return df
    df = converter_colunas_temporais(df, coluna_data, coluna_hora)
    return adicionar_mes_ano(df, coluna_data, nome_coluna)
