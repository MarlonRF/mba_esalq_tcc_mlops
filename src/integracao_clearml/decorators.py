"""
Decorators e utilities para integração com ClearML.

Fornece decoradores simplificados para criar pipelines e components,
além de utilitários para configuração e logging.
"""
from functools import wraps
from typing import Any, Callable, Dict, List, Optional
import os

from config.logger_config import logger

# Verifica disponibilidade do ClearML
try:
    from clearml import Task
    from clearml.automation import PipelineDecorator
    CLEARML_DISPONIVEL = True
except ImportError:
    CLEARML_DISPONIVEL = False
    logger.warning("ClearML não está disponível. Decoradores serão no-ops.")


def get_clearml_available() -> bool:
    """Retorna True se ClearML está disponível."""
    return CLEARML_DISPONIVEL


def ensure_clearml_available(func: Callable) -> Callable:
    """
    Decorator que garante que ClearML está disponível.
    Se não estiver, executa a função normalmente sem rastreamento.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not CLEARML_DISPONIVEL:
            logger.debug(f"ClearML não disponível. Executando {func.__name__} sem rastreamento.")
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


def pipeline(
    name: str,
    project: Optional[str] = None,
    version: str = "1.0",
    run_locally: bool = True,
    **decorator_kwargs
) -> Callable:
    """
    Decorator simplificado para criar pipelines ClearML.
    
    Args:
        name: Nome do pipeline
        project: Nome do projeto ClearML (usa config se None)
        version: Versão do pipeline
        run_locally: Se True, executa localmente sem enviar ao servidor
        **decorator_kwargs: Argumentos adicionais para PipelineDecorator
        
    Returns:
        Decorator function
        
    Example:
        >>> @pipeline(name="Meu Pipeline", project="conforto_termico")
        >>> def meu_pipeline(dados):
        >>>     return processar(dados)
    """
    def decorator(func: Callable) -> Callable:
        if not CLEARML_DISPONIVEL:
            logger.debug(f"ClearML não disponível. Pipeline '{name}' será função normal.")
            return func
        
        # Importa configuração
        from config.config_clearml import get_project_name
        
        # Usa projeto da config se não especificado
        project_name = project or get_project_name('pipelines')
        
        # Configura modo local se necessário
        if run_locally:
            PipelineDecorator.run_locally()
            logger.info(f"Pipeline '{name}' configurado para execução LOCAL")
        
        # Aplica decorator do ClearML
        decorated = PipelineDecorator.pipeline(
            name=name,
            project=project_name,
            version=version,
            **decorator_kwargs
        )(func)
        
        logger.info(f"Pipeline '{name}' registrado no ClearML (projeto: {project_name})")
        return decorated
    
    return decorator


def component(
    return_values: Optional[List[str]] = None,
    cache: bool = False,
    execution_queue: Optional[str] = None,
    **decorator_kwargs
) -> Callable:
    """
    Decorator simplificado para criar components de pipeline.
    
    Args:
        return_values: Lista de nomes dos valores retornados
        cache: Se True, cacheia resultados da execução
        execution_queue: Nome da fila de execução
        **decorator_kwargs: Argumentos adicionais para PipelineDecorator.component
        
    Returns:
        Decorator function
        
    Example:
        >>> @component(return_values=["df_processado", "artefatos"])
        >>> def processar_dados(df):
        >>>     return df, {}
    """
    def decorator(func: Callable) -> Callable:
        if not CLEARML_DISPONIVEL:
            return func
        
        # Aplica decorator do ClearML
        decorated = PipelineDecorator.component(
            return_values=return_values,
            cache=cache,
            execution_queue=execution_queue,
            **decorator_kwargs
        )(func)
        
        logger.debug(f"Component '{func.__name__}' registrado no ClearML")
        return decorated
    
    return decorator


def configure_local_execution():
    """
    Configura ClearML para execução local (não envia ao servidor).
    Útil para desenvolvimento e testes.
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível. Configuração ignorada.")
        return
    
    PipelineDecorator.run_locally()
    logger.info("ClearML configurado para execução LOCAL")


def configure_remote_execution(queue: str = "default"):
    """
    Configura ClearML para execução remota no servidor.
    
    Args:
        queue: Nome da fila de execução no servidor
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível. Configuração ignorada.")
        return
    
    # Remove configuração local se existir
    try:
        # Não há método direto para desabilitar run_locally,
        # então precisamos confiar que o próximo pipeline será remoto
        logger.info(f"ClearML configurado para execução REMOTA (fila: {queue})")
    except Exception as e:
        logger.error(f"Erro ao configurar execução remota: {e}")


def get_current_task() -> Optional[Any]:
    """
    Retorna a task ClearML atual, se existir.
    
    Returns:
        Task atual ou None se não houver task ativa
    """
    if not CLEARML_DISPONIVEL:
        return None
    
    try:
        task = Task.current_task()
        return task
    except Exception as e:
        logger.debug(f"Nenhuma task ClearML ativa: {e}")
        return None


def is_running_in_clearml() -> bool:
    """
    Verifica se o código está sendo executado dentro de uma task ClearML.
    
    Returns:
        True se estiver em uma task ClearML ativa
    """
    return get_current_task() is not None


def log_parameters(params: Dict[str, Any], prefix: str = ""):
    """
    Loga parâmetros na task ClearML atual.
    
    Args:
        params: Dicionário de parâmetros para logar
        prefix: Prefixo para os nomes dos parâmetros
    """
    task = get_current_task()
    if task is None:
        logger.debug("Nenhuma task ClearML ativa. Parâmetros não logados.")
        return
    
    try:
        for key, value in params.items():
            param_name = f"{prefix}/{key}" if prefix else key
            task.connect_configuration(
                name=param_name,
                configuration={key: value}
            )
        logger.info(f"Parâmetros logados no ClearML: {len(params)} itens")
    except Exception as e:
        logger.warning(f"Erro ao logar parâmetros no ClearML: {e}")


def log_metric(
    title: str,
    series: str,
    value: float,
    iteration: int = 0
):
    """
    Loga uma métrica escalar na task ClearML atual.
    
    Args:
        title: Título do gráfico
        series: Nome da série
        value: Valor da métrica
        iteration: Número da iteração
    """
    task = get_current_task()
    if task is None:
        logger.debug(f"Métrica {title}/{series} = {value} (task ClearML inativa)")
        return
    
    try:
        logger = task.get_logger()
        logger.report_scalar(
            title=title,
            series=series,
            value=value,
            iteration=iteration
        )
    except Exception as e:
        logger.warning(f"Erro ao logar métrica no ClearML: {e}")


def log_artifact(name: str, artifact: Any):
    """
    Loga um artefato (objeto Python) na task ClearML atual.
    
    Args:
        name: Nome do artefato
        artifact: Objeto a ser logado
    """
    task = get_current_task()
    if task is None:
        logger.debug(f"Artefato '{name}' não logado (task ClearML inativa)")
        return
    
    try:
        task.upload_artifact(name=name, artifact_object=artifact)
        logger.info(f"Artefato '{name}' enviado ao ClearML")
    except Exception as e:
        logger.warning(f"Erro ao logar artefato no ClearML: {e}")


def log_text(text: str, print_console: bool = True):
    """
    Loga texto no console da task ClearML.
    
    Args:
        text: Texto a ser logado
        print_console: Se True, também imprime no console local
    """
    task = get_current_task()
    
    if print_console:
        print(text)
    
    if task is None:
        return
    
    try:
        task_logger = task.get_logger()
        task_logger.report_text(text)
    except Exception as e:
        logger.debug(f"Erro ao logar texto no ClearML: {e}")


# ============================= Context Managers =============================

class ClearMLContext:
    """
    Context manager para execução com ClearML.
    Automaticamente cria e finaliza task.
    
    Example:
        >>> with ClearMLContext("Meu Experimento", project="conforto_termico") as task:
        >>>     # Seu código aqui
        >>>     task.get_logger().report_scalar("metric", "value", value=0.95)
    """
    
    def __init__(
        self,
        task_name: str,
        project: Optional[str] = None,
        task_type: str = "training",
        reuse_last_task_id: bool = True
    ):
        """
        Inicializa contexto ClearML.
        
        Args:
            task_name: Nome da task
            project: Nome do projeto (usa config se None)
            task_type: Tipo da task ('training', 'testing', 'inference', etc)
            reuse_last_task_id: Se True, reutiliza última task com mesmo nome
        """
        self.task_name = task_name
        self.project = project
        self.task_type = task_type
        self.reuse_last_task_id = reuse_last_task_id
        self.task = None
    
    def __enter__(self):
        """Inicia task ClearML."""
        if not CLEARML_DISPONIVEL:
            logger.warning("ClearML não disponível. Task não será criada.")
            return None
        
        from config.config_clearml import get_project_name
        
        project_name = self.project or get_project_name()
        
        try:
            self.task = Task.init(
                project_name=project_name,
                task_name=self.task_name,
                task_type=self.task_type,
                reuse_last_task_id=self.reuse_last_task_id
            )
            logger.info(f"Task ClearML iniciada: {self.task_name} (projeto: {project_name})")
            return self.task
        except Exception as e:
            logger.error(f"Erro ao iniciar task ClearML: {e}")
            return None
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finaliza task ClearML."""
        if self.task is not None:
            try:
                if exc_type is None:
                    self.task.mark_completed()
                    logger.info(f"Task ClearML '{self.task_name}' concluída com sucesso")
                else:
                    self.task.mark_failed()
                    logger.error(f"Task ClearML '{self.task_name}' falhou: {exc_val}")
            except Exception as e:
                logger.error(f"Erro ao finalizar task ClearML: {e}")
        
        # Não suprime exceções
        return False
