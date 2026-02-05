"""
Otimiza hiperparâmetros de um modelo (Classificação ou Regressão).
"""
from typing import Any, Dict, Tuple, Union
import pandas as pd
from pycaret.classification import ClassificationExperiment
from pycaret.regression import RegressionExperiment
from ..utils import extrair_info_modelo
from config.logger_config import logger


def otimizar_modelo(
    exp: Union[ClassificationExperiment, RegressionExperiment],
    tipo_problema: str,
    modelo,
    optimize: str = None,
    n_iter: int = 10,
    custom_grid: Dict = None,
) -> Tuple[Any, pd.DataFrame]:
    """
    Otimiza hiperparâmetros de um modelo usando exp.tune_model().
    Funciona tanto para classificação quanto regressão.
    
    Args:
        exp: Experimento configurado (Classification ou Regression)
        tipo_problema: 'classificacao' ou 'regressao'
        modelo: Modelo base para otimização
        optimize: Métrica a ser otimizada (ex: 'Accuracy', 'R2', 'MAE')
        n_iter: Número de iterações para a busca
        custom_grid: Grade personalizada de hiperparâmetros
        
    Returns:
        Tupla (modelo otimizado, tabela de métricas)
    """
    tipo_display = "classificação" if tipo_problema == "classificacao" else "regressão"
    logger.info(f"Otimizando hiperparâmetros do modelo de {tipo_display}...")
    
    # Obtém informações do modelo
    info = extrair_info_modelo(modelo)
    nome_modelo = info["modelo_nome"]
    
    # Define métrica padrão se não especificada
    if optimize is None:
        optimize = "Accuracy" if tipo_problema == "classificacao" else "R2"
    
    # Realiza a otimização usando o experimento
    modelo_otimizado = exp.tune_model(
        modelo,
        optimize=optimize,
        n_iter=n_iter,
        custom_grid=custom_grid,
        verbose=False
    )
    
    # Obtém métricas do modelo otimizado
    metricas = exp.pull()
    
    logger.info(f"Otimização de {tipo_display} concluída para {nome_modelo}")
    return modelo_otimizado, metricas
