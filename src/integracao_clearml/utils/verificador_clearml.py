"""
Verificação de disponibilidade do ClearML.

Funções para verificar se o ClearML está instalado e disponível.
"""
from functools import wraps
from typing import Callable
from config.logger_config import logger

# Verifica disponibilidade do ClearML
try:
    from clearml import Task
    from clearml.automation import PipelineDecorator
    CLEARML_DISPONIVEL = True
except ImportError:
    CLEARML_DISPONIVEL = False
    logger.warning("ClearML não está disponível. Funcionalidades ClearML desabilitadas.")


def obter_clearml_disponivel() -> bool:
    """
    Retorna True se ClearML está disponível.
    
    Returns:
        bool: True se ClearML está instalado e importável
        
    Example:
        >>> if obter_clearml_disponivel():
        >>>     # Usar funcionalidades ClearML
        >>>     task = Task.init(...)
    """
    return CLEARML_DISPONIVEL


def garantir_clearml_disponivel(funcao: Callable) -> Callable:
    """
    Decorator que garante que ClearML está disponível.
    Se não estiver, executa a função normalmente sem rastreamento.
    
    Args:
        funcao: Função a ser decorada
        
    Returns:
        Função decorada que verifica disponibilidade do ClearML
        
    Example:
        >>> @garantir_clearml_disponivel
        >>> def minha_funcao_clearml():
        >>>     task = Task.current_task()
        >>>     # ... código que usa ClearML
    """
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if not CLEARML_DISPONIVEL:
            logger.debug(
                f"ClearML não disponível. Executando {funcao.__name__} sem rastreamento."
            )
            return funcao(*args, **kwargs)
        return funcao(*args, **kwargs)
    return wrapper
