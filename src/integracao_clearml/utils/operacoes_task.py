"""
Operações básicas com Tasks do ClearML.

Funções para criar, buscar e gerenciar tasks.
"""
from typing import Optional, List, Any
from config.logger_config import logger
from .verificador_clearml import obter_clearml_disponivel


def criar_task(
    task_name: str,
    project_name: Optional[str] = None,
    task_type: str = "training",
    reuse_last: bool = False,
    tags: Optional[List[str]] = None
) -> Optional[Any]:
    """
    Cria uma nova task no ClearML.
    
    Args:
        task_name: Nome da task
        project_name: Nome do projeto (usa config se None)
        task_type: Tipo da task ('training', 'testing', 'data_processing', etc)
        reuse_last: Se True, reutiliza última task com mesmo nome
        tags: Lista de tags para a task
        
    Returns:
        Objeto Task ou None se ClearML não disponível
        
    Example:
        >>> task = criar_task(
        ...     task_name="Processamento de Dados",
        ...     project_name="meu_projeto",
        ...     task_type="data_processing"
        ... )
    """
    if not obter_clearml_disponivel():
        logger.warning(f"ClearML não disponível. Task '{task_name}' não criada.")
        return None
    
    from clearml import Task
    from config.config_clearml import get_project_name
    
    project = project_name or get_project_name()
    
    try:
        # IMPORTANTE: Fechar task anterior se existir
        # Isso evita o erro "Current task already created"
        try:
            task_atual = Task.current_task()
            if task_atual is not None:
                logger.info(f"Fechando task anterior: {task_atual.name}")
                task_atual.close()
        except Exception as e:
            logger.debug(f"Nenhuma task anterior para fechar: {e}")
        
        # Criar nova task
        task = Task.init(
            project_name=project,
            task_name=task_name,
            task_type=task_type,
            reuse_last_task_id=reuse_last
        )
        
        if tags:
            task.set_tags(tags)
        
        logger.info(f"Task criada: {task_name} (ID: {task.id}, Projeto: {project})")
        return task
        
    except Exception as e:
        logger.error(f"Erro ao criar task '{task_name}': {e}")
        return None


def obter_task_atual() -> Optional[Any]:
    """
    Retorna a task ClearML atualmente em execução.
    
    Returns:
        Task atual ou None se não houver task ativa
        
    Example:
        >>> task = obter_task_atual()
        >>> if task:
        >>>     task.get_logger().report_text("Mensagem de log")
    """
    if not obter_clearml_disponivel():
        return None
    
    from clearml import Task
    
    try:
        task = Task.current_task()
        if task:
            logger.debug(f"Task atual: {task.name} (ID: {task.id})")
        return task
    except Exception as e:
        logger.error(f"Erro ao obter task atual: {e}")
        return None
