import os
import tempfile
from typing import List, Optional, Union

import pandas as pd
from clearml import Dataset

from src.utils.io.io_local import save_dataframe


def download_from_clearml(
    dataset_id: str = None,
    dataset_name: str = None,
    dataset_project: str = "Datasets",
    dataset_tags: List[str] = None,
    local_path: str = "dados/dados_down_clearml.csv",
    only_published: bool = True,
) -> pd.DataFrame:
    """
    Baixa dados do ClearML.

    Args:
        dataset_id: ID do dataset no ClearML
        dataset_name: Nome do dataset (usado se dataset_id não for fornecido)
        dataset_project: Nome do projeto (usado se dataset_id não for fornecido)
        dataset_tags: Tags para filtrar (usado se dataset_id não for fornecido)
        local_path: Diretório local onde os dados serão salvos
        only_published: Se True, considera apenas datasets publicados

    Returns:
        Caminho local onde os dados foram salvos
    """
    try:
        # Obtém o dataset pelo ID ou procura pelo nome/projeto/tags
        if dataset_id:
            dataset = Dataset.get(dataset_id=dataset_id)
        else:
            if not dataset_name:
                raise ValueError("dataset_id ou dataset_name devem ser fornecidos")

            datasets = Dataset.list_datasets(
                dataset_project=dataset_project,
                dataset_name=dataset_name,
                tags=dataset_tags,
                only_published=only_published,
            )

            if not datasets:
                raise ValueError(
                    f"Nenhum dataset encontrado com os critérios: {dataset_name}, {dataset_project}"
                )

            # Pega o dataset mais recente
            dataset = datasets[-1]

        # Define o diretório local para salvar os dados (interpreta paths relativos como relativos ao cwd)
        if not local_path:
            local_path = os.path.join(os.getcwd(), "data", dataset.name)
        else:
            # se o caminho for relativo, basear no cwd
            if not os.path.isabs(local_path):
                local_path = os.path.join(os.getcwd(), local_path)

        # Baixa os arquivos do dataset
        downloaded_path = dataset.get_local_copy(local_path)
        print(f"Dataset baixado para: {downloaded_path}")

        # Se o clearml retornou um cache (por exemplo em ~/.clearml/cache/...),
        # garantimos copiar para o destino final pedido (local_path)
        try:
            import shutil

            # normalize paths
            downloaded_path_abs = os.path.abspath(downloaded_path)
            local_path_abs = os.path.abspath(local_path)

            # Se paths forem diferentes e o downloaded estiver em cache, copie
            if downloaded_path_abs != local_path_abs:
                # Se o destino existe, remove antes de copiar para garantir versão limpa
                if os.path.exists(local_path_abs):
                    if os.path.isfile(local_path_abs):
                        os.remove(local_path_abs)
                    else:
                        shutil.rmtree(local_path_abs)

                # Se o downloaded for arquivo -> copiar arquivo; se for pasta -> copiar árvore
                if os.path.isfile(downloaded_path_abs):
                    os.makedirs(os.path.dirname(local_path_abs), exist_ok=True)
                    shutil.copy2(downloaded_path_abs, local_path_abs)
                    downloaded_path_abs = local_path_abs
                else:
                    shutil.copytree(downloaded_path_abs, local_path_abs)
                    downloaded_path_abs = local_path_abs

                # Use o caminho copiado como fonte de leitura
                downloaded_path = downloaded_path_abs
        except Exception as e:
            # em caso de falha na cópia, seguir com o caminho retornado
            print(f"Aviso: Erro ao copiar arquivo: {e}")

        # Tentar localizar um arquivo tabular (csv, parquet, xlsx) no caminho retornado
        def _find_first_tabular(path: str) -> Optional[str]:
            if os.path.isfile(path):
                return path
            # procurar recursivamente por arquivos
            for root, _, files in os.walk(path):
                for f in files:
                    lf = f.lower()
                    if (
                        lf.endswith(".csv")
                        or lf.endswith(".parquet")
                        or lf.endswith(".xlsx")
                        or lf.endswith(".xls")
                    ):
                        return os.path.join(root, f)
            return None

        tabular_file = _find_first_tabular(downloaded_path)
        if tabular_file is None:
            raise Exception(
                f"Nenhum arquivo tabular (.csv/.parquet/.xlsx) encontrado em {downloaded_path}"
            )

        # Ler em DataFrame conforme extensão
        lf = tabular_file.lower()
        if lf.endswith(".csv"):
            # tentar detectar delimitador com csv.Sniffer
            import csv as _csv

            delim = None
            try:
                with open(tabular_file, "r", encoding="utf-8", errors="replace") as _f:
                    sample = _f.read(4096)
                    sniff = _csv.Sniffer()
                    delim = sniff.sniff(sample).delimiter
            except Exception:
                delim = ","

            # tentar leitura tolerante a linhas com campos a mais
            try:
                df = pd.read_csv(tabular_file, delimiter=delim, engine="python")
            except Exception:
                # fallback: usar pandas com on_bad_lines quando disponível
                try:
                    df = pd.read_csv(tabular_file, delimiter=delim, on_bad_lines="warn")
                except TypeError:
                    # pandas antigo: usar error_bad_lines=False
                    df = pd.read_csv(
                        tabular_file, delimiter=delim, error_bad_lines=False
                    )
        elif lf.endswith(".parquet"):
            df = pd.read_parquet(tabular_file)
        elif lf.endswith(".xlsx") or lf.endswith(".xls"):
            df = pd.read_excel(tabular_file)
        else:
            raise Exception(f"Formato de arquivo não suportado: {tabular_file}")

        return df
    except Exception as e:
        raise Exception(f"Erro ao baixar dados do ClearML: {str(e)}")


def download_artifact_from_clearml(
    artifact_name: str, local_path: str = None, task_id: str = None
) -> str:
    """
    Baixa um artifact do ClearML.

    Args:
        artifact_name: Nome do artifact
        local_path: Diretório local onde o artifact será salvo
        task_id: ID da tarefa (se None, usa a tarefa atual)

    Returns:
        Caminho local onde o artifact foi salvo
    """
    try:
        from clearml import Task

        # Obtém a tarefa
        if task_id:
            task = Task.get_task(task_id=task_id)
        else:
            task = Task.current_task()
            if task is None:
                raise ValueError(
                    "Nenhuma tarefa ClearML ativa encontrada e task_id não fornecido"
                )

        # Define o diretório local
        if not local_path:
            local_path = os.path.join(os.getcwd(), "artifacts", artifact_name)

        # Baixa o artifact
        artifact = task.artifacts[artifact_name]
        local_path = artifact.get_local_copy(local_path)

        return local_path
    except Exception as e:
        raise Exception(f"Erro ao baixar artifact do ClearML: {str(e)}")


def upload_dataset(
    dataset_or_path: Union[str, pd.DataFrame],
    maybe_name: Optional[str] = None,
    dataset_project: str = "Datasets",
    tags: Optional[List[str]] = None,
    dataset_name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[str]:
    """Upload flexível para ClearML.

    Formatos suportados (compatível com usos antigos):
      - upload_dataset(path_to_file_or_dir)
      - upload_dataset(path_to_file_or_dir, dataset_name)
      - upload_dataset(project_name, path_to_file)  # first arg as project, second as path
      - upload_dataset(dataframe, dataset_name)

    Retorna dataset id quando disponível.
    """
    import os

    tmp_path = None
    try:
        # Caso DataFrame: salvar temporário e usar dataset_name > maybe_name como dataset_name
        if isinstance(dataset_or_path, pd.DataFrame):
            dataset_name = dataset_name or maybe_name or "dataframe_upload"
            tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
            tmp_path = tmp.name
            tmp.close()
            save_dataframe(dataset_or_path, tmp_path)
            path = tmp_path

        else:
            # dataset_or_path é string. Resolver casos:
            # 1) maybe_name is None -> tratar primeiro argumento como caminho (deve existir)
            if maybe_name is None:
                if os.path.exists(dataset_or_path):
                    path = dataset_or_path
                    dataset_name = dataset_name or os.path.basename(dataset_or_path)
                else:
                    raise ValueError(
                        "Quando apenas um argumento string é fornecido, ele deve ser um caminho existente ou forneça maybe_name"
                    )

            else:
                # Se primeiro argumento é caminho existente -> (path, dataset_name=maybe_name)
                if os.path.exists(dataset_or_path):
                    path = dataset_or_path
                    dataset_name = dataset_name or maybe_name

                # Se segundo argumento é caminho existente -> (project, path)
                elif os.path.exists(maybe_name):
                    path = maybe_name
                    dataset_name = dataset_name or os.path.basename(maybe_name)
                    dataset_project = dataset_or_path

                else:
                    # Fallback: tratar como (path, name) mesmo que não exista (Dataset.add_files irá falhar se inválido)
                    path = dataset_or_path
                    dataset_name = maybe_name

        # Executar upload
        from clearml import Dataset

        ds = Dataset.create(
            dataset_name=dataset_name,
            dataset_project=dataset_project,
            dataset_tags=tags,
            description=description,
        )
        ds.add_files(path)
        ds.upload()
        ds.finalize()
        return getattr(ds, "id", None)

    except Exception as e:
        raise Exception(f"Erro ao subir dataset para ClearML: {e}")
    finally:
        # cleanup temporário
        if tmp_path:
            try:
                os.remove(tmp_path)
            except Exception as e:
                print(f"Aviso: Erro ao remover arquivo temporário: {e}")


def download_dataset_by_name_version(
    dataset_name: str,
    dataset_project: str = "Datasets",
    dataset_version: str | None = None,
    local_path: str | None = None,
) -> str:
    """Baixa dataset por nome/projeto e opcionalmente versão. Retorna caminho local."""
    try:
        from clearml import Dataset

        if dataset_version:
            ds = Dataset.get(
                dataset_name=dataset_name,
                dataset_project=dataset_project,
                dataset_version=str(dataset_version),
            )
        else:
            datasets = Dataset.list_datasets(
                dataset_project=dataset_project, dataset_name=dataset_name
            )
            if not datasets:
                raise ValueError("Dataset não encontrado")
            ds = datasets[-1]

        if local_path is None:
            local_path = os.path.join(os.getcwd(), "data", ds.name)

        return ds.get_local_copy(local_path)
    except Exception as e:
        raise Exception(f"Erro ao baixar dataset do ClearML: {e}")


def clearml_reachable(timeout: float = 3.0) -> bool:
    """Verifica rapidamente se o host do ClearML API está acessível usando variáveis de ambiente do client.

    Retorna True se parecer acessível, False caso contrário.
    """
    try:
        from clearml import Task

        api_host = None
        try:
            # clearml client guarda configuração em Task.get_system_tags ou em config
            from clearml.config import config

            api_host = config.get("api", "api_server", fallback=None)
        except Exception:
            api_host = None

        # fallback para variáveis de ambiente conhecidas
        import os

        if api_host is None:
            api_host = os.environ.get("CLEARML_API_HOST") or os.environ.get(
                "CLEARML_WEB_HOST"
            )

        if not api_host:
            return False

        # fazer uma requisição simples HEAD/GET
        import requests

        url = api_host.rstrip("/") + "/version"
        resp = requests.get(url, timeout=timeout)
        return resp.status_code < 500
    except Exception:
        return False
