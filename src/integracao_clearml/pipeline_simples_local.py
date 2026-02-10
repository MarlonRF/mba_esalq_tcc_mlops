"""
Pipeline ClearML Simplificado para Execucao Local
==================================================

Pipeline sem decorators de componentes que funciona localmente.
Registra apenas a task principal no ClearML.
"""

from pathlib import Path
import pandas as pd
from typing import Dict, Any
from clearml import Task, Dataset, OutputModel

# Imports dos pipelines originais
from src.pipelines.pipeline_processamento import executar_pipeline_processamento
from src.pipelines.pipeline_features import executar_pipeline_features
from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo


# Configuracao
PROJECT_NAME = "conforto_termico"
COLUNA_ALVO = "p1"
TIPO_PROBLEMA = "regressao"
METRICA_PRINCIPAL = "R2"


def executar_pipeline_local(
    caminho_csv: str,
    coluna_alvo: str = COLUNA_ALVO,
    tipo_problema: str = TIPO_PROBLEMA,
    n_modelos: int = 3,
    otimizar: bool = True,
    n_iter: int = 10
) -> Dict[str, Any]:
    """
    Pipeline completo para execucao local com tracking ClearML.
    
    Esta versao NAO usa @PipelineDecorator.component, apenas Task.init()
    para registrar a execucao no ClearML sem a complexidade dos decorators.
    
    Args:
        caminho_csv: Caminho para arquivo CSV de dados brutos
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos: Numero de modelos para comparar
        otimizar: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes de otimizacao
        
    Returns:
        Dicionario com resultados
    """
    print("="*80)
    print("PIPELINE CLEARML SIMPLIFICADO - EXECUCAO LOCAL")
    print("="*80)
    print(f"Projeto: {PROJECT_NAME}")
    print(f"Coluna alvo: {coluna_alvo}")
    print(f"Tipo: {tipo_problema}")
    print("="*80)
    
    # Criar task principal
    task = Task.init(
        project_name=PROJECT_NAME,
        task_name="Pipeline_Completo_Local",
        task_type=Task.TaskTypes.training,
        reuse_last_task_id=False,
        auto_connect_frameworks=False,
        auto_resource_monitoring=False
    )
    
    # Registrar parametros
    task.connect_configuration({
        "caminho_csv": caminho_csv,
        "coluna_alvo": coluna_alvo,
        "tipo_problema": tipo_problema,
        "n_modelos": n_modelos,
        "otimizar": otimizar,
        "n_iter": n_iter
    })
    
    logger = task.get_logger()
    
    try:
        # ====================================================================
        # ETAPA 1: UPLOAD DE DADOS BRUTOS
        # ====================================================================
        print("\n[ETAPA 1] Upload de Dados Brutos")
        print("-"*80)
        
        # Resolver caminho
        caminho_absoluto = Path(caminho_csv).resolve()
        if not caminho_absoluto.exists():
            caminho_absoluto = Path(__file__).parent.parent.parent / caminho_csv
        
        print(f"Carregando: {caminho_absoluto}")
        df_raw = pd.read_csv(caminho_absoluto)
        print(f"Dados carregados: {df_raw.shape}")
        
        # Criar dataset
        dataset_bruto = Dataset.create(
            dataset_name="dados_brutos_conforto_termico",
            dataset_project=PROJECT_NAME,
            description="Dados brutos"
        )
        
        temp_path = Path("./temp_clearml_local")
        temp_path.mkdir(exist_ok=True)
        temp_file = temp_path / "dados_brutos.csv"
        df_raw.to_csv(temp_file, index=False)
        
        dataset_bruto.add_files(str(temp_file))
        dataset_bruto.upload()
        dataset_bruto.finalize()
        
        logger.report_single_value("dataset_bruto_linhas", df_raw.shape[0])
        logger.report_single_value("dataset_bruto_colunas", df_raw.shape[1])
        
        print(f"Dataset bruto criado: {dataset_bruto.id}")
        
        # ====================================================================
        # ETAPA 2: PROCESSAMENTO
        # ====================================================================
        print("\n[ETAPA 2] Processamento de Dados")
        print("-"*80)
        
        df_processado = executar_pipeline_processamento(df_raw)
        print(f"Dados processados: {df_processado.shape}")
        
        logger.report_single_value("dataset_processado_linhas", df_processado.shape[0])
        logger.report_single_value("nas_removidos", 
                                  df_raw.isna().sum().sum() - df_processado.isna().sum().sum())
        
        # ====================================================================
        # ETAPA 3: FEATURES
        # ====================================================================
        print("\n[ETAPA 3] Engenharia de Features")
        print("-"*80)
        
        df_features, artefatos = executar_pipeline_features(df_processado)
        print(f"Dados com features: {df_features.shape}")
        
        logger.report_single_value("dataset_features_colunas", df_features.shape[1])
        
        # Upload artefatos
        if 'encoders' in artefatos:
            task.upload_artifact("encoders", artifact_object=artefatos['encoders'])
        if 'scalers' in artefatos:
            task.upload_artifact("scalers", artifact_object=artefatos['scalers'])
        
        # ====================================================================
        # ETAPA 4: TREINAMENTO
        # ====================================================================
        print("\n[ETAPA 4] Treinamento de Modelos")
        print("-"*80)
        
        # Preparar dados
        df_treino = df_features.dropna()
        print(f"Dados para treino: {df_treino.shape}")
        
        # Treinar
        resultado = treinar_pipeline_completo(
            dados=df_treino,
            coluna_alvo=coluna_alvo,
            tipo_problema=tipo_problema,
            n_modelos_comparar=n_modelos,
            otimizar_hiperparametros=otimizar,
            n_iter_otimizacao=n_iter,
            salvar_modelo_final=True,
            nome_modelo="modelo_conforto_termico_local",
            pasta_modelos="../modelos"
        )
        
        # Registrar metricas
        metricas = resultado['metricas_melhor']
        print(f"\nMetricas do melhor modelo:")
        for nome, valor in metricas.items():
            if isinstance(valor, (int, float)):
                logger.report_single_value(nome, valor)
                print(f"  {nome}: {valor:.4f}")
        
        # Upload tabela de comparacao
        tabela_comparacao = resultado['tabela_comparacao']
        task.upload_artifact("comparacao_modelos", artifact_object=tabela_comparacao)
        
        # ====================================================================
        # ETAPA 5: REGISTRO DO MODELO
        # ====================================================================
        print("\n[ETAPA 5] Registro do Modelo")
        print("-"*80)
        
        melhor_modelo_nome = str(tabela_comparacao.index[0])
        
        # Criar OutputModel
        output_model = OutputModel(
            task=task,
            name=f"modelo_{melhor_modelo_nome}_local",
            framework="PyCaret"
        )
        
        # Labels
        output_model.update_labels({
            "tipo": tipo_problema,
            "coluna_alvo": coluna_alvo,
            "melhor_modelo": melhor_modelo_nome,
            METRICA_PRINCIPAL: str(metricas.get(METRICA_PRINCIPAL, 0))
        })
        
        # Configuracao
        output_model.update_design(config_dict={
            "metricas": {k: float(v) for k, v in metricas.items() 
                        if isinstance(v, (int, float))},
            "n_features": df_treino.shape[1] - 1,
            "n_samples_treino": df_treino.shape[0]
        })
        
        # Upload arquivo do modelo
        if 'caminho_modelo' in resultado and resultado['caminho_modelo']:
            caminho_modelo = Path(resultado['caminho_modelo'])
            if caminho_modelo.exists():
                output_model.update_weights(weights_filename=str(caminho_modelo))
                print(f"Modelo registrado: {caminho_modelo.name}")
        
        # Tags
        task.add_tags([
            "local",
            melhor_modelo_nome,
            f"{METRICA_PRINCIPAL}_{metricas.get(METRICA_PRINCIPAL, 0):.2f}".replace(".", "_")
        ])
        
        # Limpar temp
        import shutil
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)
        
        # ====================================================================
        # RESUMO
        # ====================================================================
        print("\n" + "="*80)
        print("PIPELINE CONCLUIDO COM SUCESSO!")
        print("="*80)
        
        resumo = {
            "task_id": task.id,
            "dataset_bruto_id": dataset_bruto.id,
            "model_id": output_model.id if output_model else None,
            "melhor_modelo": melhor_modelo_nome,
            "metricas": {k: float(v) for k, v in metricas.items() 
                        if isinstance(v, (int, float))}
        }
        
        print(f"\nTask: {task.id}")
        print(f"Dataset: {dataset_bruto.id}")
        print(f"Modelo: {melhor_modelo_nome}")
        print(f"{METRICA_PRINCIPAL}: {metricas.get(METRICA_PRINCIPAL, 0):.4f}")
        print("\n" + "="*80)
        
        task.close()
        
        return resumo
        
    except Exception as e:
        print(f"\nERRO: {e}")
        task.mark_failed(status_message=str(e))
        task.close()
        raise
