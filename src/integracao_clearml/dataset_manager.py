"""
Gerenciamento de Datasets do ClearML.

Fornece funções para criar, buscar, baixar e gerenciar datasets no ClearML.
"""
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import os
import pandas as pd

from config.logger_config import logger

# Verifica disponibilidade do ClearML
try:
    from clearml import Dataset
    CLEARML_DISPONIVEL = True
except ImportError:
    CLEARML_DISPONIVEL = False
    logger.warning("ClearML não está disponível. Funções de dataset serão no-ops.")


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
        Objeto Dataset ou None
    """
    if not CLEARML_DISPONIVEL:
        logger.warning(f"ClearML não disponível. Dataset '{dataset_name}' não criado.")
        return None
    
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
    dataset_tags: Optional[List[str]] = None,
    only_published: bool = True
) -> Optional[Any]:
    """
    Busca um dataset no ClearML.
    
    Args:
        dataset_name: Nome do dataset
        dataset_id: ID do dataset (prioritário sobre nome)
        dataset_project: Nome do projeto
        dataset_tags: Tags para filtrar
        only_published: Se True, busca apenas datasets publicados
        
    Returns:
        Objeto Dataset ou None
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível.")
        return None
    
    from config.config_clearml import get_project_name
    
    try:
        # Busca por ID tem prioridade
        if dataset_id:
            dataset = Dataset.get(dataset_id=dataset_id)
            logger.info(f"Dataset encontrado por ID: {dataset.name} (ID: {dataset.id})")
            return dataset
        
        # Busca por nome
        if not dataset_name:
            raise ValueError("dataset_id ou dataset_name devem ser fornecidos")
        
        project = dataset_project or get_project_name('datasets')
        
        datasets = Dataset.list_datasets(
            dataset_project=project,
            dataset_name=dataset_name,
            tags=dataset_tags,
            only_published=only_published
        )
        
        if not datasets:
            logger.warning(f"Nenhum dataset encontrado: {dataset_name} (projeto: {project})")
            return None
        
        # Retorna o mais recente
        dataset = datasets[-1]
        logger.info(f"Dataset encontrado: {dataset.name} (ID: {dataset.id}, versão mais recente)")
        return dataset
        
    except Exception as e:
        logger.error(f"Erro ao buscar dataset: {e}")
        return None


def baixar_dataset(
    dataset_name: Optional[str] = None,
    dataset_id: Optional[str] = None,
    dataset_project: Optional[str] = None,
    local_path: Optional[str] = None,
    overwrite: bool = False
) -> Optional[str]:
    """
    Baixa um dataset do ClearML.
    
    Args:
        dataset_name: Nome do dataset
        dataset_id: ID do dataset
        dataset_project: Nome do projeto
        local_path: Caminho local para salvar (usa cache se None)
        overwrite: Se True, sobrescreve arquivos existentes
        
    Returns:
        Caminho local dos arquivos baixados ou None
    """
    if not CLEARML_DISPONIVEL:
        logger.warning("ClearML não disponível.")
        return None
    
    try:
        # Busca o dataset
        dataset = buscar_dataset(
            dataset_name=dataset_name,
            dataset_id=dataset_id,
            dataset_project=dataset_project
        )
        
        if dataset is None:
            return None
        
        # Define caminho local
        if local_path is None:
            # Usa cache padrão do ClearML
            caminho = dataset.get_local_copy()
        else:
            # Usa caminho especificado
            caminho = dataset.get_mutable_local_copy(
                target_folder=local_path,
                overwrite=overwrite
            )
        
        logger.info(f"Dataset baixado: {dataset.name} -> {caminho}")
        return caminho
        
    except Exception as e:
        logger.error(f"Erro ao baixar dataset: {e}")
        return None


def baixar_dataset_como_df(
    dataset_name: Optional[str] = None,
    dataset_id: Optional[str] = None,
    dataset_project: Optional[str] = None,
    arquivo_csv: str = "data.csv"
) -> Optional[pd.DataFrame]:
    """
    Baixa um dataset e retorna como DataFrame.
    
    Args:
        dataset_name: Nome do dataset
        dataset_id: ID do dataset
        dataset_project: Nome do projeto
        arquivo_csv: Nome do arquivo CSV no dataset
        
    Returns:
        DataFrame ou None
    """
    caminho_local = baixar_dataset(
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        dataset_project=dataset_project
    )
    
    if caminho_local is None:
        return None
    
    try:
        # Procura arquivo CSV
        caminho_csv = Path(caminho_local) / arquivo_csv
        
        if not caminho_csv.exists():
            # Tenta encontrar qualquer CSV
            csv_files = list(Path(caminho_local).glob("*.csv"))
            if not csv_files:
                logger.error(f"Nenhum arquivo CSV encontrado em {caminho_local}")
                return None
            caminho_csv = csv_files[0]
            logger.info(f"Usando arquivo: {caminho_csv.name}")
        
        df = pd.read_csv(caminho_csv)
        logger.info(f"DataFrame carregado: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Erro ao carregar DataFrame: {e}")
        return None


def upload_dataset(
    dataset: Any,
    arquivos: Union[str, List[str], Dict[str, str]],
    wildcard: Optional[str] = None,
    dataset_path: Optional[str] = None
):
    """
    Faz upload de arquivos para um dataset.
    
    Args:
        dataset: Objeto Dataset
        arquivos: Caminho(s) do(s) arquivo(s) ou dicionário {caminho_local: caminho_dataset}
        wildcard: Padrão wildcard para arquivos (ex: '*.csv')
        dataset_path: Caminho dentro do dataset onde salvar
    """
    if dataset is None or not CLEARML_DISPONIVEL:
        logger.warning("Dataset não disponível para upload")
        return
    
    try:
        if isinstance(arquivos, dict):
            # Upload com mapeamento de caminhos
            for local, remoto in arquivos.items():
                dataset.add_files(path=local, dataset_path=remoto)
        elif isinstance(arquivos, list):
            # Lista de arquivos
            for arquivo in arquivos:
                dataset.add_files(
                    path=arquivo,
                    wildcard=wildcard,
                    dataset_path=dataset_path
                )
        else:
            # Arquivo único ou diretório
            dataset.add_files(
                path=arquivos,
                wildcard=wildcard,
                dataset_path=dataset_path
            )
        
        logger.info(f"Arquivos adicionados ao dataset '{dataset.name}'")
        
    except Exception as e:
        logger.error(f"Erro ao fazer upload de arquivos: {e}")


def publicar_dataset(dataset: Any):
    """
    Publica um dataset (marca como finalizado e imutável).
    
    Args:
        dataset: Objeto Dataset
    """
    if dataset is None or not CLEARML_DISPONIVEL:
        return
    
    try:
        dataset.upload()
        dataset.finalize()
        logger.info(f"Dataset publicado: {dataset.name} (ID: {dataset.id})")
    except Exception as e:
        logger.error(f"Erro ao publicar dataset: {e}")


def criar_e_publicar_dataset(
    dataset_name: str,
    arquivos: Union[str, List[str]],
    dataset_project: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parent_dataset_id: Optional[str] = None
) -> Optional[str]:
    """
    Cria, faz upload e publica um dataset em uma única operação.
    
    Args:
        dataset_name: Nome do dataset
        arquivos: Caminho(s) do(s) arquivo(s)
        dataset_project: Nome do projeto
        description: Descrição
        tags: Tags
        parent_dataset_id: ID do dataset pai
        
    Returns:
        ID do dataset publicado ou None
    """
    # Cria dataset
    dataset = criar_dataset(
        dataset_name=dataset_name,
        dataset_project=dataset_project,
        description=description,
        tags=tags,
        parent_dataset_id=parent_dataset_id
    )
    
    if dataset is None:
        return None
    
    # Upload de arquivos
    upload_dataset(dataset, arquivos)
    
    # Publica
    publicar_dataset(dataset)
    
    return dataset.id


def listar_datasets(
    dataset_project: Optional[str] = None,
    tags: Optional[List[str]] = None,
    only_published: bool = True
) -> List[Dict[str, Any]]:
    """
    Lista datasets de um projeto.
    
    Args:
        dataset_project: Nome do projeto
        tags: Tags para filtrar
        only_published: Se True, lista apenas publicados
        
    Returns:
        Lista de dicionários com informações dos datasets
    """
    if not CLEARML_DISPONIVEL:
        return []
    
    from config.config_clearml import get_project_name
    
    project = dataset_project or get_project_name('datasets')
    
    try:
        datasets = Dataset.list_datasets(
            dataset_project=project,
            tags=tags,
            only_published=only_published
        )
        
        resultado = []
        for ds in datasets:
            resultado.append({
                "id": ds.id,
                "name": ds.name,
                "project": ds.project,
                "created": ds.created if hasattr(ds, 'created') else None,
                "tags": ds.tags if hasattr(ds, 'tags') else [],
            })
        
        logger.info(f"Encontrados {len(resultado)} datasets no projeto '{project}'")
        return resultado
        
    except Exception as e:
        logger.error(f"Erro ao listar datasets: {e}")
        return []


def obter_versoes_dataset(dataset_name: str, dataset_project: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Obtém todas as versões de um dataset.
    
    Args:
        dataset_name: Nome do dataset
        dataset_project: Nome do projeto
        
    Returns:
        Lista de versões ordenada (mais antiga para mais recente)
    """
    if not CLEARML_DISPONIVEL:
        return []
    
    from config.config_clearml import get_project_name
    
    project = dataset_project or get_project_name('datasets')
    
    try:
        datasets = Dataset.list_datasets(
            dataset_project=project,
            dataset_name=dataset_name,
            only_published=False
        )
        
        versoes = []
        for ds in datasets:
            versoes.append({
                "id": ds.id,
                "name": ds.name,
                "version": len(versoes) + 1,
                "created": ds.created if hasattr(ds, 'created') else None,
                "parent_datasets": ds.parent_datasets if hasattr(ds, 'parent_datasets') else []
            })
        
        logger.info(f"Encontradas {len(versoes)} versões do dataset '{dataset_name}'")
        return versoes
        
    except Exception as e:
        logger.error(f"Erro ao obter versões do dataset: {e}")
        return []


def criar_dataset_incremental(
    dataset_name: str,
    novos_arquivos: Union[str, List[str]],
    dataset_project: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Optional[str]:
    """
    Cria uma nova versão de um dataset existente (versionamento incremental).
    
    Args:
        dataset_name: Nome do dataset
        novos_arquivos: Novos arquivos a adicionar
        dataset_project: Nome do projeto
        description: Descrição da nova versão
        tags: Tags
        
    Returns:
        ID da nova versão ou None
    """
    # Busca versão mais recente
    dataset_anterior = buscar_dataset(
        dataset_name=dataset_name,
        dataset_project=dataset_project
    )
    
    parent_id = dataset_anterior.id if dataset_anterior else None
    
    # Cria nova versão
    return criar_e_publicar_dataset(
        dataset_name=dataset_name,
        arquivos=novos_arquivos,
        dataset_project=dataset_project,
        description=description or f"Versão incremental de {dataset_name}",
        tags=tags,
        parent_dataset_id=parent_id
    )


def upload_dataframe_como_dataset(
    df: pd.DataFrame,
    dataset_name: str,
    filename: str = "data.csv",
    dataset_project: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parent_dataset_id: Optional[str] = None
) -> Optional[str]:
    """
    Salva um DataFrame como CSV e faz upload para ClearML.
    
    Args:
        df: DataFrame a salvar
        dataset_name: Nome do dataset
        filename: Nome do arquivo CSV
        dataset_project: Nome do projeto
        description: Descrição
        tags: Tags
        parent_dataset_id: ID do dataset pai
        
    Returns:
        ID do dataset ou None
    """
    import tempfile
    
    # Cria arquivo temporário
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / filename
        df.to_csv(csv_path, index=False)
        
        # Upload
        dataset_id = criar_e_publicar_dataset(
            dataset_name=dataset_name,
            arquivos=str(csv_path),
            dataset_project=dataset_project,
            description=description,
            tags=tags,
            parent_dataset_id=parent_dataset_id
        )
    
    return dataset_id
