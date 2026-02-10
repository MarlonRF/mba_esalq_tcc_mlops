"""
Operações básicas com Datasets do ClearML.

Funções para criar, buscar e fazer upload de datasets.
"""
from typing import Optional, List, Any
from pathlib import Path
from config.logger_config import logger
from .verificador_clearml import obter_clearml_disponivel


def criar_dataset(
    dataset_name: str,
    dataset_project: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parent_dataset_id: Optional[str] = None
) -> Optional[Any]:
    """
    Cria um novo dataset no ClearML.
    
    Args:
        dataset_name: Nome do dataset
        dataset_project: Nome do projeto (usa config se None)
        description: Descrição do dataset
        tags: Lista de tags
        parent_dataset_id: ID do dataset pai (para versionamento)
        
    Returns:
        Objeto Dataset ou None se ClearML não disponível
        
    Example:
        >>> dataset = criar_dataset(
        ...     dataset_name="dados_processados",
        ...     description="Dados após limpeza e transformação"
        ... )
    """
    if not obter_clearml_disponivel():
        logger.warning(f"ClearML não disponível. Dataset '{dataset_name}' não criado.")
        return None
    
    from clearml import Dataset
    from config.config_clearml import get_project_name, CLEARML_DATASET_CONFIG
    
    project = dataset_project or get_project_name('datasets')
    tags = tags or CLEARML_DATASET_CONFIG.default_tags
    
    try:
        dataset = Dataset.create(
            dataset_name=dataset_name,
            dataset_project=project,
            description=description,
            parent_datasets=[parent_dataset_id] if parent_dataset_id else None
        )
        
        if tags:
            dataset.tags = tags
        
        logger.info(f"Dataset criado: {dataset_name} (ID: {dataset.id}, Projeto: {project})")
        return dataset
        
    except Exception as e:
        logger.error(f"Erro ao criar dataset '{dataset_name}': {e}")
        return None


def buscar_dataset(
    dataset_name: Optional[str] = None,
    dataset_id: Optional[str] = None,
    dataset_project: Optional[str] = None,
    only_published: bool = True
) -> Optional[Any]:
    """
    Busca um dataset no ClearML por nome ou ID.
    
    Args:
        dataset_name: Nome do dataset
        dataset_id: ID do dataset
        dataset_project: Nome do projeto
        only_published: Se True, busca apenas datasets publicados
        
    Returns:
        Objeto Dataset ou None se não encontrado
        
    Example:
        >>> dataset = buscar_dataset(dataset_name="dados_processados")
        >>> if dataset:
        >>>     caminho = dataset.get_local_copy()
    """
    if not obter_clearml_disponivel():
        logger.warning("ClearML não disponível. Não é possível buscar dataset.")
        return None
    
    from clearml import Dataset
    from config.config_clearml import get_project_name
    
    project = dataset_project or get_project_name('datasets')
    
    try:
        if dataset_id:
            dataset = Dataset.get(dataset_id=dataset_id)
        else:
            dataset = Dataset.get(
                dataset_name=dataset_name,
                dataset_project=project,
                only_published=only_published
            )
        
        logger.info(f"Dataset encontrado: {dataset.name} (ID: {dataset.id})")
        return dataset
        
    except Exception as e:
        logger.error(f"Erro ao buscar dataset: {e}")
        return None
