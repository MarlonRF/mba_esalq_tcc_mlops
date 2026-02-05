"""
Finaliza modelo treinando no dataset completo (Classificação ou Regressão).
"""
from typing import Any, Union
from pycaret.classification import ClassificationExperiment
from pycaret.regression import RegressionExperiment
from config.logger_config import logger


def finalizar_modelo(
    exp: Union[ClassificationExperiment, RegressionExperiment],
    tipo_problema: str,
    modelo
) -> Any:
    """
    Finaliza o modelo treinando-o no dataset completo (treino + validação).
    Funciona tanto para classificação quanto regressão.
    
    Esta função deve ser chamada após a validação do modelo, quando você
    está satisfeito com o desempenho e deseja treinar no dataset completo
    antes de fazer o deploy.
    
    Args:
        exp: Experimento configurado (Classification ou Regression)
        tipo_problema: 'classificacao' ou 'regressao'
        modelo: Modelo a ser finalizado
        
    Returns:
        Modelo finalizado treinado no dataset completo
    """
    tipo_display = "classificação" if tipo_problema == "classificacao" else "regressão"
    logger.info(f"Finalizando modelo de {tipo_display} no dataset completo...")
    
    modelo_final = exp.finalize_model(modelo)
    
    logger.info(f"Modelo de {tipo_display} finalizado com sucesso.")
    return modelo_final
