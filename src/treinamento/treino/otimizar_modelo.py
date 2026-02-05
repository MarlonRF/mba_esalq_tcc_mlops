"""
Otimiza hiperparâmetros de um modelo.
"""
from typing import Any, Dict, Tuple
import pandas as pd
from pycaret.classification import ClassificationExperiment
from ..utils import extrair_info_modelo
from config.logger_config import logger


def otimizar_modelo(
    exp: ClassificationExperiment,
    modelo,
    optimize: str = "Accuracy",
    n_iter: int = 10,
    custom_grid: Dict = None,
) -> Tuple[Any, pd.DataFrame]:
    """
    Otimiza hiperparâmetros de um modelo usando exp.tune_model().

    Args:
        exp (ClassificationExperiment): Experimento configurado
        modelo: Modelo base para otimização
        optimize (str): Métrica a ser otimizada
        n_iter (int): Número de iterações para a busca
        custom_grid (Dict): Grade personalizada de hiperparâmetros

    Returns:
        Tuple[Any, pd.DataFrame]: Modelo otimizado e tabela de métricas
    """
    logger.info(f"Otimizando hiperparâmetros do modelo...")

    # Obtém informações do modelo
    info = extrair_info_modelo(modelo)
    nome_modelo = info["modelo_nome"]

    # Realiza a otimização usando o experimento
    modelo_otimizado = exp.tune_model(
        modelo, optimize=optimize, n_iter=n_iter, custom_grid=custom_grid, verbose=False
    )

    # Obtém métricas do modelo otimizado
    metricas = exp.pull()

    logger.info(f"Otimização concluída para {nome_modelo}")
    return modelo_otimizado, metricas
