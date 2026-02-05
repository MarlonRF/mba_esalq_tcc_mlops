"""
Treina e seleciona os melhores modelos base (Classificação ou Regressão).
"""
from typing import Any, List, Tuple, Union
import pandas as pd
from pycaret.classification import ClassificationExperiment
from pycaret.regression import RegressionExperiment
from config.logger_config import logger


def treinar_modelo_base(
    exp: Union[ClassificationExperiment, RegressionExperiment],
    tipo_problema: str,
    n_select: int = 1,
    include: List[str] = None,
    exclude: List[str] = None,
    sort: str = None,
) -> Tuple[List[Any], pd.DataFrame]:
    """
    Treina e seleciona os melhores modelos base usando exp.compare_models().
    Funciona tanto para classificação quanto regressão.
    
    Args:
        exp: Experimento configurado (Classification ou Regression)
        tipo_problema: 'classificacao' ou 'regressao'
        n_select: Número de modelos a selecionar
        include: Lista de modelos para incluir
        exclude: Lista de modelos para excluir
        sort: Métrica para ordenação dos modelos
        
    Returns:
        Tupla (lista dos melhores modelos, tabela de comparação)
    """
    tipo_display = "classificação" if tipo_problema == "classificacao" else "regressão"
    logger.info(f"Comparando modelos de {tipo_display}...")
    
    # Treina e compara modelos usando o experimento
    melhores_modelos = exp.compare_models(
        include=include,
        exclude=exclude,
        n_select=n_select,
        sort=sort,
        verbose=False
    )
    
    # Se n_select=1, converte para lista para manter consistência
    if n_select == 1 and not isinstance(melhores_modelos, list):
        melhores_modelos = [melhores_modelos]
    
    # Obtém tabela de comparação
    tabela_comparacao = exp.pull()
    
    logger.info(f"Comparação de {tipo_display} concluída. {n_select} modelo(s) selecionado(s).")
    return melhores_modelos, tabela_comparacao
