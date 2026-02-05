"""
Realiza predições usando um modelo treinado.
"""
from typing import Any
import pandas as pd
from pycaret.classification import ClassificationExperiment
from config.logger_config import logger


def fazer_predicoes(
    exp: ClassificationExperiment,
    modelo,
    dados: pd.DataFrame,
    raw_score: bool = False,
) -> pd.DataFrame:
    """
    Realiza predições usando um modelo treinado.

    Args:
        exp (ClassificationExperiment): Experimento configurado
        modelo: Modelo treinado
        dados (pd.DataFrame): Dados para fazer predições
        raw_score (bool): Se True, retorna probabilidades brutas

    Returns:
        pd.DataFrame: DataFrame com predições e probabilidades
    """
    logger.info(f"Realizando predições em {len(dados)} amostras...")
    
    predicoes = exp.predict_model(modelo, data=dados, raw_score=raw_score)
    
    logger.info("Predições concluídas.")
    return predicoes
