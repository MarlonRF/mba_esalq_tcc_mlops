"""
Salva modelo treinado em disco.
"""
import os
from typing import Any
from pycaret.classification import ClassificationExperiment
from config.logger_config import logger


def salvar_modelo(
    exp: ClassificationExperiment,
    modelo,
    nome_modelo: str,
    pasta_destino: str = "modelos",
) -> str:
    """
    Salva modelo treinado em formato pickle.

    Args:
        exp (ClassificationExperiment): Experimento configurado
        modelo: Modelo a ser salvo
        nome_modelo (str): Nome do arquivo (sem extensão)
        pasta_destino (str): Pasta onde salvar o modelo

    Returns:
        str: Caminho completo do modelo salvo (com extensão .pkl)
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho_base = os.path.join(pasta_destino, nome_modelo)
    
    logger.info(f"Salvando modelo em: {caminho_base}.pkl")
    
    # PyCaret adiciona a extensão .pkl automaticamente
    exp.save_model(modelo, caminho_base)
    
    caminho_completo = f"{caminho_base}.pkl"
    
    logger.info(f"Modelo salvo com sucesso: {caminho_completo}")
    return caminho_completo
