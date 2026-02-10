"""
Pipeline Simples: Processamento de Dados com ClearML
"""
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any
from clearml import Task, Dataset

# NÃO usar PipelineDecorator para execução simples
# Ele envia tasks para o servidor, causando falhas se o ambiente não estiver configurado
# NÃO usar PipelineDecorator para execução simples
# Ele envia tasks para o servidor, causando falhas se o ambiente não estiver configurado

from src.pipelines.pipeline_processamento import executar_pipeline_processamento 
from src.utils.io.io_local import load_dataframe 
from config.config_custom import NOME_PROJETO


def pipeline_processamento(caminho_csv: str, project_name: str = None, offline_mode: bool = False) -> Dict[str, Any]:
    """
    Pipeline de processamento SEM decorators - execução local com tracking ClearML.
    
    Args:
        caminho_csv: Caminho para o arquivo CSV
        project_name: Nome do projeto ClearML (opcional)
        offline_mode: Se True, executa sem ClearML (apenas processamento local)
        
    Returns:
        dict com dataset_processado_id e shape
    """
    proj = project_name or NOME_PROJETO
    
    # Se modo offline, pular ClearML
    task = None
    logger = None
    
    if not offline_mode:
        try:
            print("Tentando conectar ao ClearML (timeout: 30s)...")
            import os
            os.environ['CLEARML_API_DEFAULT_REQ_METHOD'] = 'get'
            
            # Criar task manual (executa localmente mas registra no ClearML)
            task = Task.init(
                project_name=proj,
                task_name="Pipeline_01_Processamento",
                task_type=Task.TaskTypes.data_processing,
                reuse_last_task_id=False,
                auto_connect_frameworks=False
            )
            logger = task.get_logger()
            print("✓ Conectado ao ClearML")
        except Exception as e:
            print(f"⚠ Não foi possível conectar ao ClearML: {e}")
            print("Continuando em modo OFFLINE (sem tracking)...")
            offline_mode = True
            offline_mode = True
    
    if not offline_mode and task:
        task.connect_configuration({"caminho_csv": caminho_csv})
    
    try:
        print("="*80)
        print("PIPELINE 1: PROCESSAMENTO DE DADOS")
        if offline_mode:
            print("Modo: OFFLINE (sem tracking ClearML)")
        else:
            print("Modo: ONLINE (com tracking ClearML)")
        print("="*80)
        
        # Carregar - tentar múltiplos caminhos
        caminho = Path(caminho_csv)
        
        # Tentar caminho absoluto primeiro
        if not caminho.is_absolute():
            caminho = caminho.resolve()
        
        # Se não existir, tentar relativo ao projeto
        if not caminho.exists():
            caminho = Path(__file__).parent.parent.parent / caminho_csv
            
        # Última tentativa: remover '../' e procurar a partir da raiz do projeto
        if not caminho.exists():
            caminho_limpo = str(caminho_csv).replace('../', '').replace('..\\', '')
            caminho = Path(__file__).parent.parent.parent / caminho_limpo
        
        if not caminho.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {caminho_csv}\n"
                f"Tentado: {caminho}\n"
                f"Certifique-se que o arquivo existe no caminho correto."
            )
        
        print(f"\n[1] Carregando arquivo: {caminho}")
        df_raw = load_dataframe(str(caminho))
        print(f"    Shape: {df_raw.shape}")
        
        if logger:
            logger.report_single_value("dados_entrada_linhas", df_raw.shape[0])
            logger.report_single_value("dados_entrada_colunas", df_raw.shape[1])
        
        # Processar
        print(f"\n[2] Executando processamento...")
        df_processado = executar_pipeline_processamento(df_raw)
        print(f"    Shape após processamento: {df_processado.shape}")
        print(f"    NAs removidos: {df_raw.isna().sum().sum() - df_processado.isna().sum().sum()}")
        
        if logger:
            logger.report_single_value("dados_saida_linhas", df_processado.shape[0])
            logger.report_single_value("dados_saida_colunas", df_processado.shape[1])
            logger.report_single_value("nas_restantes", df_processado.isna().sum().sum())
        
        # Criar Dataset (só se não estiver em modo offline)
        dataset_id = None
        if not offline_mode:
            print(f"\n[3] Criando Dataset ClearML...")
            try:
                dataset = Dataset.create(
                    dataset_name="dados_processados",
                    dataset_project=proj
                )
                
                temp_dir = Path("./temp_clearml")
                temp_dir.mkdir(exist_ok=True)
                temp_file = temp_dir / "dados_processados.csv"
                df_processado.to_csv(temp_file, index=False)
                
                dataset.add_files(str(temp_file))
                dataset.upload()
                dataset.finalize()
                
                dataset_id = dataset.id
                print(f"    Dataset ID: {dataset_id}")
                
                # Upload sample como artefato
                if task:
                    task.upload_artifact("dados_processados_sample", df_processado.head(100))
                
                # Limpar
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"    ⚠ Erro ao criar dataset: {e}")
                print(f"    Continuando sem dataset...")
        else:
            print(f"\n[3] Modo offline - pulando criação de dataset ClearML")
        
        resultado = {
            "dataset_processado_id": dataset_id,
            "shape": df_processado.shape,
            "nas_removidos": int(df_raw.isna().sum().sum() - df_processado.isna().sum().sum()),
            "df_processado": df_processado,  # Retornar dataframe para uso direto
            "offline_mode": offline_mode
        }
        
        print("\n" + "="*80)
        print("PIPELINE 1 CONCLUÍDO!")
        print("="*80)
        if dataset_id:
            print(f"Dataset ID: {dataset_id}")
        else:
            print("Dataset: N/A (modo offline ou erro)")
        print(f"Shape: {df_processado.shape}")
        print(f"Modo: {'OFFLINE' if offline_mode else 'ONLINE'}")
        print("="*80)
        
        if task:
            task.close()
        return resultado
        
    except Exception as e:
        if task:
            task.mark_failed(status_message=str(e))
            task.close()
        raise


if __name__ == "__main__":
    resultado = pipeline_processamento(
        caminho_csv="dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv"
    )
    print(f"\nResultado: {resultado}")