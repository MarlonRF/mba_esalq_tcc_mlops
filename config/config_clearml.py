"""
Configurações centralizadas para integração com ClearML.

Define projetos, datasets, tasks e configurações padrão para rastreamento
de experimentos e versionamento de dados.
"""
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ClearMLProjectConfig:
    """Configuração de projeto ClearML."""
    
    # Projeto principal
    project_name: str = "conforto_termico"
    
    # Subprojetos
    dataset_project: str = "Datasets"
    pipeline_project: str = "Pipelines"
    experiment_project: str = "Experimentos"
    
    # Configurações de execução
    run_locally: bool = True  # True = não envia para servidor ClearML
    auto_connect_frameworks: bool = True  # Auto-detect libraries
    auto_connect_arg_parser: bool = True  # Auto-capture command-line args


@dataclass
class ClearMLDatasetConfig:
    """Configuração padrão de datasets."""
    
    # Nomes de datasets padrão
    dataset_bruto: str = "dados_brutos"
    dataset_processado: str = "dados_processados"
    dataset_features: str = "dados_features"
    dataset_treino: str = "dados_treino"
    dataset_teste: str = "dados_teste"
    
    # Tags padrão
    default_tags: List[str] = field(default_factory=lambda: [
        "conforto_termico",
        "santa_maria",
        "brasil"
    ])
    
    # Configurações de upload
    output_uri: Optional[str] = None  # None = default ClearML storage
    upload_chunk_size: int = 64 * 1024 * 1024  # 64MB


@dataclass
class ClearMLTaskConfig:
    """Configuração padrão de tasks."""
    
    # Nomes de tasks/pipelines
    task_processamento: str = "Pipeline_Processamento"
    task_features: str = "Pipeline_Features"
    task_treinamento: str = "Pipeline_Treinamento"
    task_completo: str = "Pipeline_Completo"
    task_avaliacao: str = "Avaliacao_Modelo"
    
    # Configurações de logging
    log_metrics_interval: int = 1  # Intervalo de logging (segundos)
    log_model_artifacts: bool = True
    log_plots: bool = True
    
    # Configurações de cache
    cache_task_results: bool = True
    cache_dir: str = ".clearml_cache"


@dataclass
class ClearMLModelConfig:
    """Configuração de registro de modelos."""
    
    # Nomenclatura de modelos
    model_name_prefix: str = "conforto_termico"
    model_framework: str = "pycaret"  # ou "scikit-learn"
    
    # Artefatos a salvar
    save_model_weights: bool = True
    save_model_config: bool = True
    save_model_metrics: bool = True
    save_feature_importance: bool = True
    save_plots: bool = True
    
    # Diretórios
    models_dir: str = "modelos"
    plots_dir: str = "graficos"


# ============================= Instâncias Globais =============================

# Configurações globais (podem ser sobrescritas)
CLEARML_PROJECT_CONFIG = ClearMLProjectConfig()
CLEARML_DATASET_CONFIG = ClearMLDatasetConfig()
CLEARML_TASK_CONFIG = ClearMLTaskConfig()
CLEARML_MODEL_CONFIG = ClearMLModelConfig()


# ============================= Funções Auxiliares =============================

def get_project_name(subproject: Optional[str] = None) -> str:
    """
    Retorna o nome do projeto ClearML apropriado.
    
    Args:
        subproject: Nome do subprojeto ('datasets', 'pipelines', 'experimentos')
                   Se None, retorna projeto principal
                   
    Returns:
        Nome completo do projeto
    """
    if subproject is None:
        return CLEARML_PROJECT_CONFIG.project_name
    
    subproject_map = {
        'datasets': CLEARML_PROJECT_CONFIG.dataset_project,
        'pipelines': CLEARML_PROJECT_CONFIG.pipeline_project,
        'experimentos': CLEARML_PROJECT_CONFIG.experiment_project,
        'experiments': CLEARML_PROJECT_CONFIG.experiment_project,
    }
    
    return subproject_map.get(subproject.lower(), CLEARML_PROJECT_CONFIG.project_name)


def get_dataset_name(tipo: str) -> str:
    """
    Retorna o nome padrão de dataset por tipo.
    
    Args:
        tipo: Tipo do dataset ('bruto', 'processado', 'features', 'treino', 'teste')
        
    Returns:
        Nome do dataset
    """
    dataset_map = {
        'bruto': CLEARML_DATASET_CONFIG.dataset_bruto,
        'processado': CLEARML_DATASET_CONFIG.dataset_processado,
        'features': CLEARML_DATASET_CONFIG.dataset_features,
        'treino': CLEARML_DATASET_CONFIG.dataset_treino,
        'teste': CLEARML_DATASET_CONFIG.dataset_teste,
    }
    
    return dataset_map.get(tipo.lower(), tipo)


def get_task_name(tipo: str) -> str:
    """
    Retorna o nome padrão de task por tipo.
    
    Args:
        tipo: Tipo da task ('processamento', 'features', 'treinamento', 'completo', 'avaliacao')
        
    Returns:
        Nome da task
    """
    task_map = {
        'processamento': CLEARML_TASK_CONFIG.task_processamento,
        'features': CLEARML_TASK_CONFIG.task_features,
        'treinamento': CLEARML_TASK_CONFIG.task_treinamento,
        'completo': CLEARML_TASK_CONFIG.task_completo,
        'avaliacao': CLEARML_TASK_CONFIG.task_avaliacao,
    }
    
    return task_map.get(tipo.lower(), tipo)


def get_model_name(model_type: str, timestamp: Optional[str] = None) -> str:
    """
    Gera nome padronizado para modelo.
    
    Args:
        model_type: Tipo do modelo (ex: 'RandomForest', 'XGBoost')
        timestamp: Timestamp opcional (default: usa timestamp atual)
        
    Returns:
        Nome do modelo formatado
    """
    from datetime import datetime
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    prefix = CLEARML_MODEL_CONFIG.model_name_prefix
    return f"{prefix}_{model_type}_{timestamp}"


def configure_clearml_from_env():
    """
    Configura ClearML usando variáveis de ambiente.
    
    Variáveis esperadas:
    - CLEARML_PROJECT_NAME: Nome do projeto principal
    - CLEARML_DATASET_PROJECT: Nome do projeto de datasets
    - CLEARML_RUN_LOCALLY: True/False para execução local
    - CLEARML_API_HOST: Host da API ClearML
    - CLEARML_WEB_HOST: Host web ClearML
    - CLEARML_FILES_HOST: Host de arquivos ClearML
    """
    global CLEARML_PROJECT_CONFIG, CLEARML_DATASET_CONFIG, CLEARML_TASK_CONFIG
    
    # Atualiza projeto
    if project_name := os.getenv("CLEARML_PROJECT_NAME"):
        CLEARML_PROJECT_CONFIG.project_name = project_name
    
    if dataset_project := os.getenv("CLEARML_DATASET_PROJECT"):
        CLEARML_PROJECT_CONFIG.dataset_project = dataset_project
    
    # Atualiza modo de execução
    run_locally = os.getenv("CLEARML_RUN_LOCALLY", "true").lower() == "true"
    CLEARML_PROJECT_CONFIG.run_locally = run_locally
    
    # Atualiza cache
    if cache_dir := os.getenv("CLEARML_CACHE_DIR"):
        CLEARML_TASK_CONFIG.cache_dir = cache_dir


def get_clearml_config_summary() -> Dict:
    """Retorna resumo das configurações atuais."""
    return {
        "project": {
            "main": CLEARML_PROJECT_CONFIG.project_name,
            "datasets": CLEARML_PROJECT_CONFIG.dataset_project,
            "pipelines": CLEARML_PROJECT_CONFIG.pipeline_project,
            "experiments": CLEARML_PROJECT_CONFIG.experiment_project,
        },
        "execution": {
            "run_locally": CLEARML_PROJECT_CONFIG.run_locally,
            "auto_connect": CLEARML_PROJECT_CONFIG.auto_connect_frameworks,
        },
        "datasets": {
            "default_tags": CLEARML_DATASET_CONFIG.default_tags,
        },
        "tasks": {
            "cache_enabled": CLEARML_TASK_CONFIG.cache_task_results,
            "cache_dir": CLEARML_TASK_CONFIG.cache_dir,
        },
        "models": {
            "framework": CLEARML_MODEL_CONFIG.model_framework,
            "models_dir": CLEARML_MODEL_CONFIG.models_dir,
        }
    }


# Inicialização automática das configurações a partir do ambiente
configure_clearml_from_env()
