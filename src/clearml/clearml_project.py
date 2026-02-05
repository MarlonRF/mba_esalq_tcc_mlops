from typing import Optional

from clearml import Dataset, Task
from clearml.backend_api.session.client import APIClient


def obter_ou_criar_id_projeto(
    nome_do_projeto: str, criar_se_nao_existir: bool = False
) -> Optional[str]:
    """
    Busca o ID de um projeto no ClearML pelo nome. Se o projeto não existir,
    pode opcionalmente criar um novo.

    Args:
        nome_do_projeto (str): O nome exato do projeto a ser buscado ou criado.
        criar_se_nao_existir (bool): Se True (padrão), cria um novo projeto caso
                                     ele não seja encontrado. Se False, apenas
                                     retorna None se o projeto não existir.

    Returns:
        Optional[str]: O ID do projeto encontrado ou criado, ou None se o projeto
                       não for encontrado e a criação estiver desativada.
    """
    try:
        client = APIClient()

        # Busca todos os projetos e cria um dicionário mapeando nome para ID
        todos_os_projetos = client.projects.get_all()
        mapa_de_projetos = {p.name: p.id for p in todos_os_projetos if p}

        # Verifica se o projeto já existe no mapa
        id_projeto = mapa_de_projetos.get(nome_do_projeto)

        if id_projeto:
            print(f"Projeto '{nome_do_projeto}' encontrado. ID: {id_projeto}")
            return id_projeto

        # Se o projeto não foi encontrado, verifica a flag de criação
        if criar_se_nao_existir:
            print(
                f"Projeto '{nome_do_projeto}' não encontrado. Criando novo projeto..."
            )
            # Se não existir e a criação for permitida, cria o projeto
            novo_projeto = client.projects.create(project_name=nome_do_projeto)
            print(
                f"Projeto '{nome_do_projeto}' criado com sucesso. ID: {novo_projeto.id}"
            )
            return novo_projeto.id
        else:
            # Se não for para criar, apenas informa e retorna None
            print(
                f"Projeto '{nome_do_projeto}' não encontrado. A opção para criar novos projetos está desativada."
            )
            return None

    except Exception as e:
        print(f"Ocorreu um erro ao interagir com a API do ClearML: {e}")
        return None


def buscar_dataset(
    nome_do_dataset: str, nome_do_projeto: Optional[str] = None
) -> Optional[str]:
    """
    Busca a versão mais recente de um dataset no ClearML pelo nome e, opcionalmente,
    pelo nome do projeto.

    Args:
        nome_do_dataset (str): O nome exato do dataset a ser buscado.
        nome_do_projeto (Optional[str]): O nome do projeto onde o dataset está localizado.
                                         Se None, busca em todos os projetos.

    Returns:
        Optional[str]: O ID do dataset encontrado, ou None caso não seja encontrado.
    """
    try:
        print(f"\nBuscando dataset '{nome_do_dataset}' no projeto '{nome_do_projeto}' ")

        # Se parece um dataset_id (por exemplo contém '-' ou é longo), tente por id primeiro
        is_possible_id = ("-" in nome_do_dataset) or (len(nome_do_dataset) >= 20)

        if is_possible_id:
            try:
                dataset = Dataset.get(dataset_id=nome_do_dataset)
                print(f"Dataset encontrado por id. ID: {dataset.id}")
                return dataset.id
            except Exception as e:
                # se falhar buscando por id, continuará tentando por nome
                print(f"Aviso: Erro ao buscar dataset por ID: {e}")

        # busca por nome (comportamento antigo)
        dataset = Dataset.get(
            dataset_name=nome_do_dataset, dataset_project=nome_do_projeto
        )
        print(f"Dataset '{nome_do_dataset}' encontrado. ID: {dataset.id}")
        return dataset.id
    except ValueError:
        print(
            f"Dataset '{nome_do_dataset}' não foi encontrado no projeto especificado."
        )
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao buscar o dataset: {e}")
        return None


def buscar_task(
    nome_da_task: str, nome_do_projeto: Optional[str] = None
) -> Optional[str]:
    """
    Busca a execução mais recente de uma task no ClearML.

    Args:
        nome_da_task (str): O nome exato da task a ser buscada.
        nome_do_projeto (str): O nome do projeto onde o pipeline está localizado.

    Returns:
        Optional[str]: O ID do pipeline encontrado, ou None caso não seja encontrado.
    """
    try:
        client = APIClient()
        lista_tasks = client.tasks.get_all()
        mapa_de_tasks = {t.name: t.id for t in lista_tasks if t}
        task_id = mapa_de_tasks.get(nome_da_task)
        return task_id

    except Exception as e:
        print(f"Ocorreu um erro ao buscar a task: {e}")
        return None
