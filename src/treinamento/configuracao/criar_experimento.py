"""
Factory para criar experimentos PyCaret (Classificação ou Regressão).
"""
from typing import Dict, Optional, Union
import pandas as pd
from pycaret.classification import ClassificationExperiment
from pycaret.regression import RegressionExperiment
from config.config_gerais import PARAMS_PADRAO
from config.logger_config import logger


def criar_experimento(
    dados: pd.DataFrame,
    coluna_alvo: str,
    tipo_problema: str,
    params: Optional[Dict] = None
) -> Union[ClassificationExperiment, RegressionExperiment]:
    """
    Factory para criar e configurar um experimento PyCaret (Classificação ou Regressão).
    
    Args:
        dados: Dados para treinamento
        coluna_alvo: Nome da coluna alvo (variável dependente)
        tipo_problema: 'classificacao' ou 'regressao'
        params: Parâmetros adicionais para o setup
        
    Returns:
        ClassificationExperiment ou RegressionExperiment configurado
        
    Raises:
        ValueError: Se tipo_problema não for 'classificacao' ou 'regressao'
    """
    # Valida tipo de problema
    if tipo_problema not in ["classificacao", "regressao"]:
        raise ValueError(
            f"tipo_problema deve ser 'classificacao' ou 'regressao', "
            f"recebido: {tipo_problema}"
        )
    
    # Instancia experimento apropriado
    if tipo_problema == "classificacao":
        exp = ClassificationExperiment()
        logger.info("Criando experimento de CLASSIFICAÇÃO...")
    else:
        exp = RegressionExperiment()
        logger.info("Criando experimento de REGRESSÃO...")
    
    # Prepara parâmetros
    setup_params = PARAMS_PADRAO.copy()
    if params:
        setup_params.update(params)
    
    # Adiciona dados e target
    setup_params["data"] = dados
    setup_params["target"] = coluna_alvo
    
    # Configura o experimento
    logger.info(f"Configurando experimento de {tipo_problema}...")
    exp.setup(**setup_params)
    
    logger.info(f"✓ Experimento de {tipo_problema} configurado com sucesso")
    return exp
