"""
Gerenciamento de Tasks do ClearML.

Fornece funções para criar, buscar, conectar e gerenciar tasks ClearML.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime

from config.logger_config import logger

# Verifica disponibilidade do ClearML
try:
    from clearml import Task
    from clearml.backend_api.session.client import APIClient
    CLEARML_DISPONIVEL = True
except ImportError:
    CLEARML_DISPONIVEL = False
    logger.warning("ClearML não está disponível. Funções de task serão no-ops.")


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
        task_type: Tipo da task ('training', 'testing', 'inference', etc)
        reuse_last: Se True, reutiliza última task com mesmo nome
        tags: Lista de tags para a task
        
    Returns:
        Objeto Task ou None se ClearML não disponível
    """
    if not CLEARML_DISPONIVEL:
        logger.warning(f"ClearML não disponível. Task '{task_name}' não criada.")
        return None
    
    from config.config_clearml import get_project_name
    
    project = project_name or get_project_name()
    
    try:
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
        Task atual ou None
    """
    if not CLEARML_DISPONIVEL:
        return None
    
    try:
        task = Task.current_task()
        if task:
            logger.debug(f"Task atual: {task.name} (ID: {task.id})")
        return task
    except Exception as e:
        logger.debug(f"Nenhuma task ativa: {e}")
        return None


def buscar_task_por_nome(
    nome_task: str,
    nome_projeto: Optional[str] = None,
    apenas_completas: bool = False
) -> Optional[str]:
    """
    Busca uma task pelo nome e retorna seu ID.
    
    Args:
        nome_task: Nome da task a buscar
        nome_projeto: Nome do projeto (opcional, filtra por projeto)
        apenas_completas: Se True, busca apenas tasks completadas
        
    Returns:
        ID da task encontrada ou None
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível.")
        return None
    
    try:
        client = APIClient()
        
        # Parâmetros de busca
        filtros = {"name": nome_task}
        if nome_projeto:
            # Primeiro busca o ID do projeto
            projetos = client.projects.get_all()
            projeto_map = {p.name: p.id for p in projetos if p}
            if nome_projeto in projeto_map:
                filtros["project"] = [projeto_map[nome_projeto]]
        
        if apenas_completas:
            filtros["status"] = ["completed"]
        
        # Busca tasks
        tasks = client.tasks.get_all(**filtros)
        
        if not tasks:
            logger.warning(f"Nenhuma task encontrada com nome '{nome_task}'")
            return None
        
        # Retorna a task mais recente
        task_mais_recente = sorted(tasks, key=lambda t: t.created, reverse=True)[0]
        logger.info(f"Task encontrada: {task_mais_recente.name} (ID: {task_mais_recente.id})")
        
        return task_mais_recente.id
        
    except Exception as e:
        logger.error(f"Erro ao buscar task '{nome_task}': {e}")
        return None


def buscar_task_por_id(task_id: str) -> Optional[Any]:
    """
    Busca uma task pelo ID.
    
    Args:
        task_id: ID da task
        
    Returns:
        Objeto Task ou None
    """
    if not CLEARML_DISPONIVEL:
        return None
    
    try:
        task = Task.get_task(task_id=task_id)
        logger.info(f"Task recuperada: {task.name} (ID: {task.id})")
        return task
    except Exception as e:
        logger.error(f"Erro ao buscar task por ID '{task_id}': {e}")
        return None


def listar_tasks_projeto(
    nome_projeto: str,
    status: Optional[List[str]] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Lista todas as tasks de um projeto.
    
    Args:
        nome_projeto: Nome do projeto
        status: Lista de status para filtrar (ex: ['completed', 'running'])
        limit: Número máximo de tasks a retornar
        
    Returns:
        Lista de dicionários com informações das tasks
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível.")
        return []
    
    try:
        client = APIClient()
        
        # Busca ID do projeto
        projetos = client.projects.get_all()
        projeto_map = {p.name: p.id for p in projetos if p}
        
        if nome_projeto not in projeto_map:
            logger.warning(f"Projeto '{nome_projeto}' não encontrado")
            return []
        
        projeto_id = projeto_map[nome_projeto]
        
        # Parâmetros de busca
        filtros = {"project": [projeto_id]}
        if status:
            filtros["status"] = status
        
        # Busca tasks
        tasks = client.tasks.get_all(**filtros)
        tasks = tasks[:limit]  # Limita número de resultados
        
        # Formata resultado
        resultado = []
        for task in tasks:
            resultado.append({
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "type": task.type,
                "created": task.created,
                "completed": task.completed if hasattr(task, 'completed') else None,
                "project": nome_projeto,
            })
        
        logger.info(f"Encontradas {len(resultado)} tasks no projeto '{nome_projeto}'")
        return resultado
        
    except Exception as e:
        logger.error(f"Erro ao listar tasks do projeto '{nome_projeto}': {e}")
        return []


def conectar_parametros(task: Any, parametros: Dict[str, Any]):
    """
    Conecta parâmetros à task ClearML.
    
    Args:
        task: Objeto Task
        parametros: Dicionário de parâmetros
    """
    if task is None or not CLEARML_DISPONIVEL:
        return
    
    try:
        task.connect(parametros)
        logger.info(f"Parâmetros conectados à task: {len(parametros)} itens")
    except Exception as e:
        logger.error(f"Erro ao conectar parâmetros: {e}")


def conectar_configuracao(
    task: Any,
    nome_config: str,
    configuracao: Dict[str, Any]
):
    """
    Conecta uma configuração à task ClearML.
    
    Args:
        task: Objeto Task
        nome_config: Nome da configuração
        configuracao: Dicionário de configuração
    """
    if task is None or not CLEARML_DISPONIVEL:
        return
    
    try:
        task.connect_configuration(
            name=nome_config,
            configuration=configuracao
        )
        logger.info(f"Configuração '{nome_config}' conectada à task")
    except Exception as e:
        logger.error(f"Erro ao conectar configuração: {e}")


def registrar_metrica(
    task: Any,
    titulo: str,
    serie: str,
    valor: float,
    iteracao: int = 0
):
    """
    Registra uma métrica escalar na task.
    
    Args:
        task: Objeto Task
        titulo: Título do gráfico
        serie: Nome da série
        valor: Valor da métrica
        iteracao: Número da iteração
    """
    if task is None or not CLEARML_DISPONIVEL:
        logger.debug(f"Métrica {titulo}/{serie} = {valor} (não registrada)")
        return
    
    try:
        logger_clearml = task.get_logger()
        logger_clearml.report_scalar(
            title=titulo,
            series=serie,
            value=valor,
            iteration=iteracao
        )
    except Exception as e:
        logger.error(f"Erro ao registrar métrica: {e}")


def registrar_metricas_dict(
    task: Any,
    metricas: Dict[str, float],
    titulo: str = "Métricas",
    iteracao: int = 0
):
    """
    Registra múltiplas métricas de um dicionário.
    
    Args:
        task: Objeto Task
        metricas: Dicionário {nome_metrica: valor}
        titulo: Título do grupo de métricas
        iteracao: Número da iteração
    """
    if task is None or not CLEARML_DISPONIVEL:
        logger.debug(f"Métricas não registradas: {list(metricas.keys())}")
        return
    
    for nome, valor in metricas.items():
        if isinstance(valor, (int, float)):
            registrar_metrica(task, titulo, nome, float(valor), iteracao)


def registrar_artefato(
    task: Any,
    nome: str,
    artefato: Any,
    metadata: Optional[Dict] = None
):
    """
    Registra um artefato na task.
    
    Args:
        task: Objeto Task
        nome: Nome do artefato
        artefato: Objeto a ser registrado
        metadata: Metadados opcionais
    """
    if task is None or not CLEARML_DISPONIVEL:
        logger.debug(f"Artefato '{nome}' não registrado")
        return
    
    try:
        task.upload_artifact(
            name=nome,
            artifact_object=artefato,
            metadata=metadata
        )
        logger.info(f"Artefato '{nome}' registrado na task")
    except Exception as e:
        logger.error(f"Erro ao registrar artefato '{nome}': {e}")


def registrar_texto(task: Any, texto: str):
    """
    Registra texto no console da task.
    
    Args:
        task: Objeto Task
        texto: Texto a registrar
    """
    if task is None or not CLEARML_DISPONIVEL:
        return
    
    try:
        logger_clearml = task.get_logger()
        logger_clearml.report_text(texto)
    except Exception as e:
        logger.error(f"Erro ao registrar texto: {e}")


def finalizar_task(task: Any, sucesso: bool = True):
    """
    Finaliza uma task marcando-a como completa ou falhada.
    
    Args:
        task: Objeto Task
        sucesso: True para marcar como completa, False para falha
    """
    if task is None or not CLEARML_DISPONIVEL:
        return
    
    try:
        if sucesso:
            task.mark_completed()
            logger.info(f"Task '{task.name}' marcada como COMPLETA")
        else:
            task.mark_failed()
            logger.warning(f"Task '{task.name}' marcada como FALHA")
    except Exception as e:
        logger.error(f"Erro ao finalizar task: {e}")


def clonar_task(
    task_id: str,
    novo_nome: Optional[str] = None,
    novo_projeto: Optional[str] = None
) -> Optional[str]:
    """
    Clona uma task existente.
    
    Args:
        task_id: ID da task a clonar
        novo_nome: Nome para a nova task (usa nome original se None)
        novo_projeto: Projeto para a nova task (usa projeto original se None)
        
    Returns:
        ID da task clonada ou None
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível.")
        return None
    
    try:
        task_original = Task.get_task(task_id=task_id)
        
        # Clona a task
        task_clonada = Task.clone(
            source_task=task_original,
            name=novo_nome,
            project=novo_projeto
        )
        
        logger.info(f"Task clonada: {task_clonada.name} (ID: {task_clonada.id})")
        return task_clonada.id
        
    except Exception as e:
        logger.error(f"Erro ao clonar task '{task_id}': {e}")
        return None


def obter_parametros_task(task_id: str) -> Dict[str, Any]:
    """
    Obtém os parâmetros de uma task.
    
    Args:
        task_id: ID da task
        
    Returns:
        Dicionário com os parâmetros
    """
    if not CLEARML_DISPONIVEL:
        return {}
    
    try:
        task = Task.get_task(task_id=task_id)
        parametros = task.get_parameters()
        
        logger.info(f"Parâmetros recuperados da task '{task.name}': {len(parametros)} itens")
        return parametros
        
    except Exception as e:
        logger.error(f"Erro ao obter parâmetros da task '{task_id}': {e}")
        return {}


def obter_artefato_task(
    task_id: str,
    nome_artefato: str
) -> Optional[Any]:
    """
    Obtém um artefato de uma task.
    
    Args:
        task_id: ID da task
        nome_artefato: Nome do artefato
        
    Returns:
        Artefato ou None
    """
    if not CLEARML_DISPONIVEL:
        return None
    
    try:
        task = Task.get_task(task_id=task_id)
        artefato = task.artifacts[nome_artefato].get()
        
        logger.info(f"Artefato '{nome_artefato}' recuperado da task '{task.name}'")
        return artefato
        
    except Exception as e:
        logger.error(f"Erro ao obter artefato '{nome_artefato}' da task '{task_id}': {e}")
        return None
