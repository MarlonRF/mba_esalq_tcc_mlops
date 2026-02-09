"""
Módulo de integração com ClearML.

Fornece ferramentas completas para rastreamento de experimentos, versionamento
de datasets e execução de pipelines com ClearML.

Módulos:
--------
- decorators: Decoradores para pipelines e components
- task_manager: Gerenciamento de tasks
- dataset_manager: Gerenciamento de datasets
- pipeline_processamento_clearml: Pipeline de processamento rastreado
- registrar_modelo_clearml: Registro de modelos

Uso Básico:
-----------
```python
# Importações principais
from src.clearml import (
    pipeline, component,  # Decoradores
    criar_task, buscar_dataset,  # Gerenciadores
    ClearMLContext  # Context manager
)

# Exemplo 1: Criar pipeline decorado
@pipeline(name="Meu Pipeline", project="conforto_termico")
def meu_pipeline(dados):
    resultado = processar(dados)
    return resultado

# Exemplo 2: Usar context manager
with ClearMLContext("Meu Experimento", project="conforto_termico") as task:
    task.get_logger().report_scalar("metrica", "valor", value=0.95)

# Exemplo 3: Gerenciar datasets
dataset_id = criar_e_publicar_dataset(
    dataset_name="meus_dados",
    arquivos="dados/arquivo.csv",
    tags=["treinamento"]
)
```

Configuração:
------------
As configurações são centralizadas em config/config_clearml.py e podem ser
sobrescritas por variáveis de ambiente:

- CLEARML_PROJECT_NAME: Nome do projeto principal
- CLEARML_DATASET_PROJECT: Projeto para datasets
- CLEARML_RUN_LOCALLY: True para execução local
"""

# ============================= Decoradores =============================
from .decorators import (
    # Decoradores principais
    pipeline,
    component,
    
    # Utilitários de configuração
    configure_local_execution,
    configure_remote_execution,
    get_clearml_available,
    is_running_in_clearml,
    get_current_task,
    
    # Logging
    log_parameters,
    log_metric,
    log_artifact,
    log_text,
    
    # Context manager
    ClearMLContext,
)

# ============================= Gerenciadores =============================
from .task_manager import (
    # Criação e busca
    criar_task,
    obter_task_atual,
    buscar_task_por_nome,
    buscar_task_por_id,
    listar_tasks_projeto,
    
    # Operações
    conectar_parametros,
    conectar_configuracao,
    registrar_metrica,
    registrar_metricas_dict,
    registrar_artefato,
    registrar_texto,
    finalizar_task,
    
    # Avançado
    clonar_task,
    obter_parametros_task,
    obter_artefato_task,
)

from .dataset_manager import (
    # Criação e busca
    criar_dataset,
    buscar_dataset,
    baixar_dataset,
    baixar_dataset_como_df,
    
    # Upload
    upload_dataset,
    publicar_dataset,
    criar_e_publicar_dataset,
    upload_dataframe_como_dataset,
    
    # Listagem e versionamento
    listar_datasets,
    obter_versoes_dataset,
    criar_dataset_incremental,
)

# ============================= Pipeline Completo (Decorators) =============================
# Pipeline principal com @PipelineDecorator.pipeline e @PipelineDecorator.component
# Arquivo: pipeline_completo_decorators.py
# Uso: from src.clearml.pipeline_completo_decorators import executar_pipeline

# ============================= Registro de Modelos =============================
from .registrar_modelo_clearml import (
    registrar_modelo_clearml,
)

# ============================= Exports =============================
__all__ = [
    # Decoradores
    'pipeline',
    'component',
    'configure_local_execution',
    'configure_remote_execution',
    'get_clearml_available',
    'is_running_in_clearml',
    'get_current_task',
    'log_parameters',
    'log_metric',
    'log_artifact',
    'log_text',
    'ClearMLContext',
    
    # Task Manager
    'criar_task',
    'obter_task_atual',
    'buscar_task_por_nome',
    'buscar_task_por_id',
    'listar_tasks_projeto',
    'conectar_parametros',
    'conectar_configuracao',
    'registrar_metrica',
    'registrar_metricas_dict',
    'registrar_artefato',
    'registrar_texto',
    'finalizar_task',
    'clonar_task',
    'obter_parametros_task',
    'obter_artefato_task',
    
    # Dataset Manager
    'criar_dataset',
    'buscar_dataset',
    'baixar_dataset',
    'baixar_dataset_como_df',
    'upload_dataset',
    'publicar_dataset',
    'criar_e_publicar_dataset',
    'upload_dataframe_como_dataset',
    'listar_datasets',
    'obter_versoes_dataset',
    'criar_dataset_incremental',
    
    # Modelos
    'registrar_modelo_clearml',
]


# ============================= Utilitários de Conveniência =============================

def inicializar_clearml(run_locally: bool = True):
    """
    Inicializa ClearML com configurações padrão.
    
    Args:
        run_locally: Se True, configura para execução local
    """
    if run_locally:
        configure_local_execution()
    
    from config.logger_config import logger
    logger.info("ClearML inicializado")


def verificar_disponibilidade() -> bool:
    """
    Verifica se ClearML está disponível e configurado.
    
    Returns:
        True se ClearML está disponível
    """
    disponivel = get_clearml_available()
    
    if disponivel:
        from config.logger_config import logger
        logger.info("✅ ClearML disponível e pronto")
    else:
        from config.logger_config import logger
        logger.warning("⚠️  ClearML não disponível")
    
    return disponivel


def obter_resumo_configuracao() -> dict:
    """
    Retorna resumo das configurações atuais do ClearML.
    
    Returns:
        Dicionário com configurações
    """
    from config.config_clearml import get_clearml_config_summary
    return get_clearml_config_summary()


# Inicialização automática
if get_clearml_available():
    from config.logger_config import logger
    logger.info("Módulo ClearML carregado com sucesso")
