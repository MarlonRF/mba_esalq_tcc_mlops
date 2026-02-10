"""
Registra um modelo treinado no ClearML.
"""
import os
from typing import Any, Dict, Optional
from pycaret.classification import ClassificationExperiment
from src.treinamento.utils import extrair_info_modelo
from config.logger_config import logger

try:
    from clearml import OutputModel, Task
    CLEARML_DISPONIVEL = True
except ImportError:
    OutputModel = Any  # type: ignore[assignment]
    Task = Any  # type: ignore[assignment]
    CLEARML_DISPONIVEL = False
    logger.warning("ClearML não está disponível. Registro de modelo será ignorado.")


def registrar_modelo_clearml(
    exp: ClassificationExperiment,
    task: Task,
    modelo,
    nome_modelo: str,
    metricas: Dict[str, float],
    pasta_output: str = "modelo_final",
) -> Optional[OutputModel]:
    """
    Registra um modelo treinado no ClearML com suas métricas.

    Args:
        exp (ClassificationExperiment): Experimento PyCaret
        task (Task): Tarefa ClearML atual
        modelo: Modelo treinado para registrar
        nome_modelo (str): Nome para o modelo registrado
        metricas (Dict[str, float]): Dicionário com métricas do modelo
        pasta_output (str): Pasta para salvar o modelo

    Returns:
        OutputModel: Objeto de modelo ClearML registrado
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível. Modelo não será registrado no servidor.")
        return None

    # Garante que a pasta de saída existe
    os.makedirs(pasta_output, exist_ok=True)

    # Define o caminho para salvar o modelo
    caminho_modelo = os.path.join(pasta_output, nome_modelo)

    # Salva o modelo usando PyCaret (sem extensão, PyCaret adiciona .pkl)
    exp.save_model(modelo, caminho_modelo)
    
    # Adiciona extensão .pkl ao caminho
    caminho_modelo_pkl = f"{caminho_modelo}.pkl"

    # Registra o modelo no ClearML
    output_model = OutputModel(
        task=task,
        name=nome_modelo,
        framework="scikit-learn",
        config_dict=extrair_info_modelo(modelo)["parametros"],
    )

    # Registra o arquivo do modelo
    output_model.update_weights(
        weights_filename=caminho_modelo_pkl,
        target_filename=nome_modelo,
        auto_delete_file=False,
    )

    # Registra as métricas
    for nome_metrica, valor in metricas.items():
        output_model.report_scalar(
            title="Métricas de Validação", series=nome_metrica, value=valor
        )

    return output_model
