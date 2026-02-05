"""
Finaliza modelo treinando no dataset completo.
"""
from typing import Any
from pycaret.classification import ClassificationExperiment
from config.logger_config import logger


def finalizar_modelo(exp: ClassificationExperiment, modelo) -> Any:
    """
    Finaliza o modelo treinando-o no dataset completo (treino + validação).

    Esta função deve ser chamada após a validação do modelo, quando você
    está satisfeito com o desempenho e deseja treinar no dataset completo
    antes de fazer o deploy.

    Args:
        exp (ClassificationExperiment): Experimento configurado
        modelo: Modelo a ser finalizado

    Returns:
        Any: Modelo finalizado treinado no dataset completo
    """
    logger.info("Finalizando modelo no dataset completo...")
    
    modelo_final = exp.finalize_model(modelo)
    
    logger.info("Modelo finalizado com sucesso.")
    return modelo_final
