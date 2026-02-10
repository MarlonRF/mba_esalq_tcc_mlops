"""
Integração de artefatos com ClearML.

Funções para registrar dataframes, métricas, gráficos e outros artefatos.
"""
from typing import Optional, Dict, Any, Union
import pandas as pd
from pathlib import Path
from config.logger_config import logger
from .verificador_clearml import obter_clearml_disponivel
from .operacoes_task import obter_task_atual


def registrar_dataframe(
    df: pd.DataFrame,
    nome: str,
    descricao: Optional[str] = None,
    task: Optional[Any] = None
) -> bool:
    """
    Registra um DataFrame como artefato no ClearML.
    
    Args:
        df: DataFrame a ser registrado
        nome: Nome do artefato
        descricao: Descrição opcional
        task: Task ClearML (usa task atual se None)
        
    Returns:
        True se registrado com sucesso, False caso contrário
        
    Example:
        >>> df_processado = pd.DataFrame(...)
        >>> registrar_dataframe(df_processado, "dados_processados")
    """
    if not obter_clearml_disponivel():
        logger.debug(f"ClearML não disponível. DataFrame '{nome}' não registrado.")
        return False
    
    task = task or obter_task_atual()
    if not task:
        logger.warning(f"Nenhuma task ativa. DataFrame '{nome}' não registrado.")
        return False
    
    try:
        task.upload_artifact(nome, artifact_object=df)
        logger.info(f"DataFrame registrado: {nome} (shape: {df.shape})")
        return True
    except Exception as e:
        logger.error(f"Erro ao registrar DataFrame '{nome}': {e}")
        return False


def registrar_metricas(
    metricas: Dict[str, Union[float, int]],
    task: Optional[Any] = None
) -> bool:
    """
    Registra métricas no ClearML.
    
    Args:
        metricas: Dicionário com nome_metrica: valor
        task: Task ClearML (usa task atual se None)
        
    Returns:
        True se registrado com sucesso, False caso contrário
        
    Example:
        >>> metricas = {"acuracia": 0.95, "f1_score": 0.93}
        >>> registrar_metricas(metricas)
    """
    if not obter_clearml_disponivel():
        logger.debug("ClearML não disponível. Métricas não registradas.")
        return False
    
    task = task or obter_task_atual()
    if not task:
        logger.warning("Nenhuma task ativa. Métricas não registradas.")
        return False
    
    try:
        logger_task = task.get_logger()
        for nome, valor in metricas.items():
            logger_task.report_single_value(nome, valor)
        
        logger.info(f"Métricas registradas: {list(metricas.keys())}")
        return True
    except Exception as e:
        logger.error(f"Erro ao registrar métricas: {e}")
        return False


def registrar_arquivo(
    caminho: Union[str, Path],
    nome: Optional[str] = None,
    task: Optional[Any] = None
) -> bool:
    """
    Registra um arquivo como artefato no ClearML.
    
    Args:
        caminho: Caminho do arquivo
        nome: Nome do artefato (usa nome do arquivo se None)
        task: Task ClearML (usa task atual se None)
        
    Returns:
        True se registrado com sucesso, False caso contrário
        
    Example:
        >>> registrar_arquivo("modelo.pkl", "modelo_treinado")
    """
    if not obter_clearml_disponivel():
        logger.debug("ClearML não disponível. Arquivo não registrado.")
        return False
    
    task = task or obter_task_atual()
    if not task:
        logger.warning("Nenhuma task ativa. Arquivo não registrado.")
        return False
    
    caminho = Path(caminho)
    if not caminho.exists():
        logger.error(f"Arquivo não encontrado: {caminho}")
        return False
    
    nome = nome or caminho.name
    
    try:
        task.upload_artifact(nome, artifact_object=str(caminho))
        logger.info(f"Arquivo registrado: {nome}")
        return True
    except Exception as e:
        logger.error(f"Erro ao registrar arquivo '{nome}': {e}")
        return False
