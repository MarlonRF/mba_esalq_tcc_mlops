"""
Treina e seleciona os melhores modelos base.
"""
from typing import Any, List, Tuple
import pandas as pd
from pycaret.classification import ClassificationExperiment
from config.logger_config import logger

def treinar_modelo_base(
    exp: ClassificationExperiment,
    n_select: int = 1,
    include: List[str] = None,
    exclude: List[str] = None,
    sort: str = None,
) -> Tuple[List[Any], pd.DataFrame]:
    """
    Treina e seleciona os melhores modelos base usando exp.compare_models().

    Args:
        exp (ClassificationExperiment): Experimento configurado
        n_select (int): Número de modelos a selecionar
        include (List[str]): Lista de modelos para incluir
        exclude (List[str]): Lista de modelos para excluir
        sort (str): Métrica para ordenação dos modelos

    Returns:
        Tuple[List, pd.DataFrame]: Lista dos melhores modelos e tabela de comparação
    """
    logger.info(f"Comparando modelos de classificação...")

    # Treina e compara modelos usando o experimento
    melhores_modelos = exp.compare_models(
        include=include, exclude=exclude, n_select=n_select, sort=sort, verbose=False
    )

    # Se n_select=1, converte para lista para manter consistência
    if n_select == 1 and not isinstance(melhores_modelos, list):
        melhores_modelos = [melhores_modelos]

    # Obtém tabela de comparação
    tabela_comparacao = exp.pull()

    logger.info(f"Comparação concluída. {n_select} modelo(s) selecionado(s).")
    return melhores_modelos, tabela_comparacao
