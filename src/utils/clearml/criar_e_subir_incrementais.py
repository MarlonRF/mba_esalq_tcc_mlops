"""
Cria versões incrementais de datasets no ClearML.
"""
import os
from typing import Dict, List, Optional

try:
    from clearml import Dataset
    CLEARML_AVAILABLE = True
except Exception:
    CLEARML_AVAILABLE = False


def criar_e_subir_incrementais(
    caminhos_csv: Dict[int, str],
    nome_dataset: str,
    projeto_dataset: str,
    tags: List[str] | None = None,
    dataset_pai_id: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Para cada CSV em `caminhos_csv` (chave=tamanho), cria uma versão no ClearML.

    Mantém a genealogia via parent_datasets. Retorna lista de info sobre versões criadas.
    """
    if not CLEARML_AVAILABLE:
        raise RuntimeError(
            "ClearML não está disponível. Instale clearml para usar essa função."
        )

    info_versoes = []
    # ordena por tamanho
    # garantir projeto no ClearML antes do loop
    from utils.clearml_project import ensure_project
    proj = ensure_project(projeto_dataset)
    if proj is None:
        raise RuntimeError(
            "Não foi possível garantir existência do projeto ClearML. Verifique a conexão/configuração do ClearML."
        )
    for tam in sorted(caminhos_csv.keys()):
        caminho = caminhos_csv[tam]

        if dataset_pai_id is None:
            ds = Dataset.create(
                dataset_name=nome_dataset,
                dataset_project=projeto_dataset,
                dataset_version=str(tam),
                dataset_tags=tags or [],
            )
        else:
            ds = Dataset.create(
                dataset_name=nome_dataset,
                dataset_project=projeto_dataset,
                dataset_version=str(tam),
                parent_datasets=[dataset_pai_id],
                dataset_tags=tags or [],
            )

        # adiciona arquivo ou pasta
        if os.path.isdir(caminho):
            ds.add_files(caminho)
        else:
            ds.add_files(path=caminho)

        ds.upload()
        ds.finalize()

        info = {
            "tamanho": str(tam),
            "dataset_id": getattr(ds, "id", None),
            "caminho": caminho,
        }
        info_versoes.append(info)

        # atualiza parent para próxima versão
        dataset_pai_id = getattr(ds, "id", None)

    return info_versoes
