"""
Cria e configura um experimento de classificação no PyCaret.
"""
from typing import Dict, Optional
import pandas as pd
from pycaret.classification import ClassificationExperiment
from config.config_gerais import PARAMS_PADRAO
from config.logger_config import logger


def criar_experimento_classificacao(
    dados: pd.DataFrame, coluna_alvo: str, params: Optional[Dict] = None
) -> ClassificationExperiment:
    """
    Cria e configura um experimento de classificação no PyCaret.

    Args:
        dados (pd.DataFrame): Dados para treinamento
        coluna_alvo (str): Nome da coluna alvo (variável dependente)
        params (Dict, opcional): Parâmetros adicionais para o setup

    Returns:
        ClassificationExperiment: Experimento configurado
    """
    # Inicializa experimento
    exp = ClassificationExperiment()

    # Prepara parâmetros
    setup_params = PARAMS_PADRAO.copy()
    if params:
        setup_params.update(params)

    # Adiciona dados e target
    setup_params["data"] = dados
    setup_params["target"] = coluna_alvo

    # Configura o experimento
    logger.info("Configurando experimento de classificação...")
    exp.setup(**setup_params)

    return exp
