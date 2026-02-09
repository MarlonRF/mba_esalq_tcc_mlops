"""
Pipeline 2: Engenharia de Features
===================================

Pipeline independente que:
1. Carrega dados processados (do Dataset ou arquivo)
2. Executa engenharia de features
3. Salva dados com features como novo Dataset
"""

from pathlib import Path
import pandas as pd
from typing import Dict, Any, Optional
from clearml import Task, Dataset
from config.config_custom import NOME_PROJETO
 
from src.pipelines.pipeline_features import executar_pipeline_features
from src.utils.io.io_local import load_dataframe


PROJECT_NAME_DEFAULT = "conforto_termico"


def pipeline_features(
    dataset_processado_id: Optional[str] = None,
    caminho_csv: Optional[str] = None,
    project_name: str = None
) -> Dict[str, Any]:
    """
    Pipeline de engenharia de features com ClearML.
    
    Args:
        dataset_processado_id: ID do dataset processado (prioritario)
        caminho_csv: Caminho alternativo se nao usar dataset
        project_name: Nome do projeto ClearML (usa default se None)
        
    Returns:
        dict com dataset_features_id e informacoes dos artefatos
    """
    # Definir projeto
    proj_name = project_name or PROJECT_NAME_DEFAULT
    
    # Criar task
    task = Task.init(
        project_name=proj_name,
        task_name="Pipeline_02_Features",
        task_type=Task.TaskTypes.data_processing,
        reuse_last_task_id=False,
        auto_connect_frameworks=False
    )
    
    task.connect_configuration({
        "dataset_processado_id": dataset_processado_id,
        "caminho_csv": caminho_csv
    })
    logger = task.get_logger()
    
    print("="*80)
    print("PIPELINE 2: ENGENHARIA DE FEATURES")
    print("="*80)
    
    try:
        # Carregar dados
        if dataset_processado_id:
            print(f"\n[1] Baixando Dataset: {dataset_processado_id}")
            dataset = Dataset.get(dataset_id=dataset_processado_id)
            local_path = dataset.get_local_copy()
            csv_files = list(Path(local_path).glob("*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"Nenhum CSV encontrado em {local_path}")
            df_processado = load_dataframe(str(csv_files[0]))
        elif caminho_csv:
            print(f"\n[1] Carregando arquivo: {caminho_csv}")
            caminho_absoluto = Path(caminho_csv).resolve()
            if not caminho_absoluto.exists():
                caminho_absoluto = Path(__file__).parent.parent.parent / caminho_csv
            df_processado = load_dataframe(str(caminho_absoluto))
        else:
            raise ValueError("Forneça dataset_processado_id OU caminho_csv")
        
        print(f"    Shape: {df_processado.shape}")
        logger.report_single_value("dados_entrada_linhas", df_processado.shape[0])
        logger.report_single_value("dados_entrada_colunas", df_processado.shape[1])
        
        # Engenharia de features
        print("\n[2] Executando engenharia de features...")
        df_features, artefatos = executar_pipeline_features(df_processado)
        print(f"    Shape apos features: {df_features.shape}")
        print(f"    Novas colunas: {df_features.shape[1] - df_processado.shape[1]}")
        
        logger.report_single_value("dados_saida_colunas", df_features.shape[1])
        logger.report_single_value("novas_features", df_features.shape[1] - df_processado.shape[1])
        
        # Upload artefatos
        print("\n[3] Registrando artefatos...")
        for nome, artefato in artefatos.items():
            task.upload_artifact(nome, artifact_object=artefato)
            print(f"    - {nome}")
        
        # Dataset com features
        print("\n[4] Criando Dataset de features...")
        dataset_features = Dataset.create(
            dataset_name="dados_features",
            dataset_project=proj_name,
            parent_datasets=[dataset_processado_id] if dataset_processado_id else None
        )
        
        temp_path = Path("./temp_clearml")
        temp_path.mkdir(exist_ok=True)
        temp_file = temp_path / "dados_features.csv"
        df_features.to_csv(temp_file, index=False)
        dataset_features.add_files(str(temp_file))
        dataset_features.upload()
        dataset_features.finalize()
        
        print(f"    Dataset ID: {dataset_features.id}")
        
        # Limpar
        import shutil
        shutil.rmtree(temp_path, ignore_errors=True)
        
        # Resumo
        resultado = {
            "dataset_features_id": dataset_features.id,
            "colunas_entrada": df_processado.shape[1],
            "colunas_saida": df_features.shape[1],
            "novas_features": df_features.shape[1] - df_processado.shape[1],
            "artefatos": list(artefatos.keys())
        }
        
        task.upload_artifact("dados_features_sample", df_features.head(100))
        
        print("\n" + "="*80)
        print("PIPELINE 2 CONCLUIDO!")
        print("="*80)
        print(f"Dataset features: {dataset_features.id}")
        print(f"Colunas: {df_processado.shape[1]} -> {df_features.shape[1]}")
        print(f"Artefatos: {', '.join(artefatos.keys())}")
        print("="*80)
        
        task.close()
        return resultado
        
    except Exception as e:
        task.mark_failed(status_message=str(e))
        task.close()
        raise


if __name__ == "__main__":
    # Exemplo de uso com dataset
    resultado = pipeline_features(
        dataset_processado_id="COLE_AQUI_O_ID_DO_DATASET_PROCESSADO"
    )
    print(f"\nResultado: {resultado}")
