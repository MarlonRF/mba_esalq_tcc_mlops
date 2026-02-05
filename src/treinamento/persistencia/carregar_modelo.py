"""
Carrega modelo salvo do disco.
"""
from typing import Any
from pycaret.classification import load_model
from config.logger_config import logger


def carregar_modelo(caminho_modelo: str) -> Any:
    """
    Carrega modelo salvo em formato pickle.

    Args:
        caminho_modelo (str): Caminho do modelo (com ou sem extensão .pkl)

    Returns:
        Any: Modelo carregado
    """
    # Remove extensão .pkl se fornecida (PyCaret já adiciona)
    if caminho_modelo.endswith('.pkl'):
        caminho_modelo = caminho_modelo[:-4]
    
    logger.info(f"Carregando modelo de: {caminho_modelo}")
    
    modelo = load_model(caminho_modelo)
    
    logger.info("Modelo carregado com sucesso.")
    return modelo
