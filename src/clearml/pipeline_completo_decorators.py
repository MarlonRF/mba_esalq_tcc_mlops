"""
Pipeline Completo ClearML com Decorators
=========================================

Pipeline completo usando @PipelineDecorator.pipeline e @PipelineDecorator.component
para rastreamento total de MLOps: datasets, tasks, modelos, metricas e artefatos.

Este arquivo usa os decorators oficiais do ClearML para criar uma pipeline
orquestrada que pode ser executada localmente ou remotamente.
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple
import shutil

# Imports ClearML
from clearml import Task, Dataset, OutputModel, PipelineDecorator

# Imports dos pipelines originais
from src.pipelines.pipeline_processamento import executar_pipeline_processamento
from src.pipelines.pipeline_features import executar_pipeline_features
from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo


# ============================================================================
# CONFIGURAcaO GLOBAL
# ============================================================================
PROJECT_NAME = "conforto_termico"
COLUNA_ALVO = "p1"
TIPO_PROBLEMA = "regressao"
METRICA_PRINCIPAL = "R2"  # Metrica para decidir modelo vigente


# ============================================================================
# COMPONENTE 1: UPLOAD DE DADOS BRUTOS
# ============================================================================
@PipelineDecorator.component(
    return_values=["dataset_id", "df_shape"],
    cache=True,
    task_type=Task.TaskTypes.data_processing
)
def component_upload_dados_brutos(
    caminho_csv: str,
    dataset_name: str = "dados_brutos_conforto_termico"
) -> Tuple[str, Tuple[int, int]]:
    """
    Carrega dados brutos e faz upload para ClearML como Dataset.
    
    Args:
        caminho_csv: Caminho para o arquivo CSV de dados brutos
        dataset_name: Nome do dataset no ClearML
        
    Returns:
        dataset_id: ID do dataset criado
        df_shape: Shape do DataFrame (linhas, colunas)
    """
    print(f"\n{'='*80}")
    print(f"[COMPONENTE 1] Upload de Dados Brutos")
    print(f"{'='*80}")
    
    # Resolver caminho absoluto
    caminho_absoluto = Path(caminho_csv).resolve()
    if not caminho_absoluto.exists():
        # Tentar caminho relativo ao diretorio do script
        caminho_absoluto = Path(__file__).parent.parent.parent / caminho_csv
        if not caminho_absoluto.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado: {caminho_csv}")
    
    print(f"Carregando dados de: {caminho_absoluto}")
    
    # Carregar dados
    df_raw = pd.read_csv(caminho_absoluto)
    print(f"Dados carregados: {df_raw.shape}")
    
    # Criar dataset
    dataset = Dataset.create(
        dataset_name=dataset_name,
        dataset_project=PROJECT_NAME,
        description="Dados brutos de conforto termico de Santa Maria/RS"
    )
    
    # Salvar temporariamente
    temp_path = Path("./temp_clearml")
    temp_path.mkdir(exist_ok=True)
    temp_file = temp_path / "dados_brutos.csv"
    df_raw.to_csv(temp_file, index=False)
    
    # Upload
    dataset.add_files(str(temp_file))
    dataset.upload()
    dataset.finalize()
    
    # Limpar
    shutil.rmtree(temp_path, ignore_errors=True)
    
    print(f"Dataset criado: {dataset.id}")
    print(f"  - Shape: {df_raw.shape}")
    print(f"  - Colunas: {len(df_raw.columns)}")
    
    return dataset.id, df_raw.shape


# ============================================================================
# COMPONENTE 2: PIPELINE DE PROCESSAMENTO
# ============================================================================
@PipelineDecorator.component(
    return_values=["dataset_id", "metricas_processamento"],
    cache=True,
    task_type=Task.TaskTypes.data_processing
)
def component_pipeline_processamento(
    dataset_bruto_id: str,
    dataset_name: str = "dados_processados_conforto_termico"
) -> Tuple[str, Dict[str, Any]]:
    """
    Executa pipeline de processamento e registra dados processados.
    
    Args:
        dataset_bruto_id: ID do dataset de dados brutos
        dataset_name: Nome do dataset processado
        
    Returns:
        dataset_id: ID do dataset processado
        metricas_processamento: Metricas do processamento
    """
    print(f"\n{'='*80}")
    print(f"[COMPONENTE 2] Pipeline de Processamento")
    print(f"{'='*80}")
    
    # Baixar dataset bruto
    dataset_bruto = Dataset.get(dataset_id=dataset_bruto_id)
    local_path = dataset_bruto.get_local_copy()
    
    # Carregar dados
    csv_files = list(Path(local_path).glob("*.csv"))
    df_raw = pd.read_csv(csv_files[0])
    print(f"Dados brutos carregados: {df_raw.shape}")
    
    # Executar processamento
    print("Executando processamento...")
    df_processado = executar_pipeline_processamento(df_raw)
    
    # Calcular metricas
    metricas = {
        "linhas_entrada": int(df_raw.shape[0]),
        "linhas_saida": int(df_processado.shape[0]),
        "colunas_entrada": int(df_raw.shape[1]),
        "colunas_saida": int(df_processado.shape[1]),
        "nas_removidos": int(df_raw.isna().sum().sum() - df_processado.isna().sum().sum()),
        "taxa_retencao": float(df_processado.shape[0] / df_raw.shape[0])
    }
    
    # Registrar metricas na task atual
    task = Task.current_task()
    if task:
        logger = task.get_logger()
        for nome, valor in metricas.items():
            logger.report_single_value(nome, valor)
    
    print(f"Dados processados: {df_processado.shape}")
    print(f"  - NAs removidos: {metricas['nas_removidos']}")
    print(f"  - Taxa retencao: {metricas['taxa_retencao']:.2%}")
    
    # Criar dataset processado
    dataset_processado = Dataset.create(
        dataset_name=dataset_name,
        dataset_project=PROJECT_NAME,
        parent_datasets=[dataset_bruto_id],
        description="Dados processados (limpeza, imputacao aplicada)"
    )
    
    # Salvar e upload
    temp_path = Path("./temp_clearml")
    temp_path.mkdir(exist_ok=True)
    temp_file = temp_path / "dados_processados.csv"
    df_processado.to_csv(temp_file, index=False)
    
    dataset_processado.add_files(str(temp_file))
    dataset_processado.upload()
    dataset_processado.finalize()
    
    # Limpar
    shutil.rmtree(temp_path, ignore_errors=True)
    
    print(f"Dataset processado criado: {dataset_processado.id}")
    
    return dataset_processado.id, metricas


# ============================================================================
# COMPONENTE 3: PIPELINE DE FEATURES
# ============================================================================
@PipelineDecorator.component(
    return_values=["dataset_id", "artefatos_features"],
    cache=True,
    task_type=Task.TaskTypes.data_processing
)
def component_pipeline_features(
    dataset_processado_id: str,
    dataset_name: str = "dados_features_conforto_termico"
) -> Tuple[str, Dict[str, Any]]:
    """
    Executa pipeline de features e registra dados com features derivadas.
    
    Args:
        dataset_processado_id: ID do dataset processado
        dataset_name: Nome do dataset com features
        
    Returns:
        dataset_id: ID do dataset com features
        artefatos_features: Artefatos criados (encoders, scalers, etc)
    """
    print(f"\n{'='*80}")
    print(f"[COMPONENTE 3] Pipeline de Features")
    print(f"{'='*80}")
    
    # Baixar dataset processado
    dataset_proc = Dataset.get(dataset_id=dataset_processado_id)
    local_path = dataset_proc.get_local_copy()
    
    # Carregar dados
    csv_files = list(Path(local_path).glob("*.csv"))
    df_proc = pd.read_csv(csv_files[0])
    print(f"Dados processados carregados: {df_proc.shape}")
    
    # Executar pipeline de features
    print("Executando pipeline de features...")
    df_feat, artefatos = executar_pipeline_features(
        df_proc,
        aplicar_codificacao=True,
        metodo_codificacao='label',
        criar_features_derivadas=True,
        tipos_features_derivadas=['imc', 'imc_classe', 'heat_index', 'dew_point', 't*u'],
        aplicar_normalizacao=True,
        metodo_normalizacao='standard',
        agrupamento_normalizacao='mes-ano'
    )
    
    print(f"Features criadas: {df_feat.shape}")
    print(f"  - Artefatos: {list(artefatos.keys())}")
    
    # Registrar artefatos na task
    task = Task.current_task()
    if task:
        for nome, artefato in artefatos.items():
            task.upload_artifact(nome, artifact_object=artefato)
    
    # Criar dataset com features
    dataset_features = Dataset.create(
        dataset_name=dataset_name,
        dataset_project=PROJECT_NAME,
        parent_datasets=[dataset_processado_id],
        description="Dados com features derivadas e normalizadas"
    )
    
    # Salvar e upload
    temp_path = Path("./temp_clearml")
    temp_path.mkdir(exist_ok=True)
    temp_file = temp_path / "dados_features.csv"
    df_feat.to_csv(temp_file, index=False)
    
    dataset_features.add_files(str(temp_file))
    dataset_features.upload()
    dataset_features.finalize()
    
    # Limpar
    shutil.rmtree(temp_path, ignore_errors=True)
    
    print(f"Dataset com features criado: {dataset_features.id}")
    
    # Serializar artefatos para retorno
    artefatos_info = {k: str(type(v).__name__) for k, v in artefatos.items()}
    
    return dataset_features.id, artefatos_info


# ============================================================================
# COMPONENTE 4: PIPELINE DE TREINAMENTO
# ============================================================================
@PipelineDecorator.component(
    return_values=["resultado_treinamento", "caminho_modelo"],
    cache=False,  # Nao fazer cache de treinamento
    task_type=Task.TaskTypes.training
)
def component_pipeline_treinamento(
    dataset_features_id: str,
    coluna_alvo: str,
    tipo_problema: str,
    n_modelos: int = 3,
    otimizar: bool = True,
    n_iter: int = 10
) -> Tuple[Dict[str, Any], str]:
    """
    Executa pipeline de treinamento e registra modelo.
    
    Args:
        dataset_features_id: ID do dataset com features
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos: Numero de modelos para comparar
        otimizar: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes para otimizacao
        
    Returns:
        resultado_treinamento: Dicionario com resultados
        caminho_modelo: Caminho do modelo salvo
    """
    print(f"\n{'='*80}")
    print(f"[COMPONENTE 4] Pipeline de Treinamento")
    print(f"{'='*80}")
    
    # Baixar dataset com features
    dataset_feat = Dataset.get(dataset_id=dataset_features_id)
    local_path = dataset_feat.get_local_copy()
    
    # Carregar dados
    csv_files = list(Path(local_path).glob("*.csv"))
    df_feat = pd.read_csv(csv_files[0])
    print(f"Dados com features carregados: {df_feat.shape}")
    
    # Remover NAs
    df_treino = df_feat.dropna()
    print(f"Dados para treino (sem NAs): {df_treino.shape}")
    
    # Executar treinamento
    print(f"\nExecutando treinamento...")
    print(f"  - Coluna alvo: {coluna_alvo}")
    print(f"  - Tipo: {tipo_problema}")
    print(f"  - Modelos: {n_modelos}")
    print(f"  - Otimizar: {otimizar}")
    
    resultado = treinar_pipeline_completo(
        dados=df_treino,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        n_modelos_comparar=n_modelos,
        otimizar_hiperparametros=otimizar,
        n_iter_otimizacao=n_iter,
        salvar_modelo_final=True,
        nome_modelo="modelo_conforto_termico_pipeline",
        pasta_modelos="./modelos_pipeline"
    )
    
    # Extrair informacoes
    metricas = resultado['metricas_melhor']
    tabela_comparacao = resultado['tabela_comparacao']
    melhor_modelo_nome = str(tabela_comparacao.index[0])
    caminho_modelo = resultado.get('caminho_modelo', '')
    
    print(f"\nTreinamento concluido!")
    print(f"  - Melhor modelo: {melhor_modelo_nome}")
    print(f"  - {METRICA_PRINCIPAL}: {metricas.get(METRICA_PRINCIPAL, 0):.4f}")
    
    # Registrar metricas na task
    task = Task.current_task()
    if task:
        logger = task.get_logger()
        
        # Metricas escalares
        for nome, valor in metricas.items():
            if isinstance(valor, (int, float)):
                logger.report_single_value(nome, valor)
        
        # Tabela de comparacao
        task.upload_artifact("comparacao_modelos", artifact_object=tabela_comparacao)
        
        # Grafico de comparacao
        fig, ax = plt.subplots(figsize=(12, 6))
        metricas_plot = ['MAE', 'MSE', 'RMSE', 'R2'] if tipo_problema == 'regressao' else ['Accuracy', 'AUC', 'F1']
        metricas_disponiveis = [m for m in metricas_plot if m in tabela_comparacao.columns]
        
        if metricas_disponiveis:
            tabela_comparacao[metricas_disponiveis].plot(kind='bar', ax=ax)
            ax.set_title('Comparacao de Modelos - Metricas')
            ax.set_xlabel('Modelos')
            ax.set_ylabel('Valor')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            logger.report_matplotlib_figure(
                title="Comparacao_Modelos",
                series="Metricas",
                figure=fig,
                iteration=0
            )
            plt.close()
    
    # Preparar resultado para retorno
    resultado_serializado = {
        'melhor_modelo': melhor_modelo_nome,
        'metricas': {k: float(v) if isinstance(v, (int, float)) else str(v) 
                     for k, v in metricas.items()},
        'n_modelos_testados': len(tabela_comparacao),
        'metrica_principal': METRICA_PRINCIPAL,
        'valor_metrica_principal': float(metricas.get(METRICA_PRINCIPAL, 0))
    }
    
    return resultado_serializado, str(caminho_modelo)


# ============================================================================
# COMPONENTE 5: REGISTRO DO MODELO
# ============================================================================
@PipelineDecorator.component(
    return_values=["model_id"],
    cache=False,
    task_type=Task.TaskTypes.service
)
def component_registrar_modelo(
    resultado_treinamento: Dict[str, Any],
    caminho_modelo: str,
    dataset_features_id: str
) -> str:
    """
    Registra modelo no ClearML com metadados completos.
    
    Args:
        resultado_treinamento: Resultados do treinamento
        caminho_modelo: Caminho do arquivo do modelo
        dataset_features_id: ID do dataset usado no treinamento
        
    Returns:
        model_id: ID do modelo registrado
    """
    print(f"\n{'='*80}")
    print(f"[COMPONENTE 5] Registro do Modelo")
    print(f"{'='*80}")
    
    task = Task.current_task()
    
    # Criar OutputModel
    melhor_modelo = resultado_treinamento['melhor_modelo']
    output_model = OutputModel(
        task=task,
        name=f"modelo_{melhor_modelo}_conforto_termico",
        framework="PyCaret"
    )
    
    # Labels
    output_model.update_labels({
        "tipo": TIPO_PROBLEMA,
        "coluna_alvo": COLUNA_ALVO,
        "melhor_modelo": melhor_modelo,
        "metrica_principal": METRICA_PRINCIPAL,
        f"{METRICA_PRINCIPAL}": str(resultado_treinamento['valor_metrica_principal'])
    })
    
    # Design (configuracao e metricas)
    output_model.update_design(config_dict={
        "metricas": resultado_treinamento['metricas'],
        "dataset_id": dataset_features_id,
        "n_modelos_testados": resultado_treinamento['n_modelos_testados']
    })
    
    # Upload do arquivo do modelo
    caminho = Path(caminho_modelo)
    if caminho.exists():
        output_model.update_weights(weights_filename=str(caminho))
        print(f"Modelo registrado: {caminho.name}")
    else:
        print(f"AVISO: Arquivo do modelo nao encontrado: {caminho}")
    
    print(f"OutputModel criado")
    print(f"  - Nome: {output_model.name}")
    print(f"  - Framework: PyCaret")
    print(f"  - {METRICA_PRINCIPAL}: {resultado_treinamento['valor_metrica_principal']:.4f}")
    
    return output_model.id if hasattr(output_model, 'id') else "N/A"


# ============================================================================
# PIPELINE COMPLETO
# ============================================================================
@PipelineDecorator.pipeline(
    name="Pipeline_Completo_Conforto_Termico",
    project=PROJECT_NAME,
    version="1.0.0",
    add_pipeline_tags=True
)
def pipeline_completo_clearml(
    caminho_csv: str,
    coluna_alvo: str = COLUNA_ALVO,
    tipo_problema: str = TIPO_PROBLEMA,
    n_modelos: int = 3,
    otimizar: bool = True,
    n_iter: int = 10
) -> Dict[str, Any]:
    """
    Pipeline Completo de MLOps com ClearML.
    
    Executa todas as etapas do pipeline de ML com rastreamento completo:
    1. Upload de dados brutos
    2. Processamento de dados
    3. Engenharia de features
    4. Treinamento de modelos
    5. Registro do melhor modelo
    
    Args:
        caminho_csv: Caminho para arquivo CSV de dados brutos
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos: Numero de modelos para comparar
        otimizar: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes de otimizacao
        
    Returns:
        Dicionario com IDs de todos os recursos criados
    """
    print(f"\n{'='*80}")
    print(f"PIPELINE COMPLETO - CLEARML")
    print(f"{'='*80}")
    print(f"Projeto: {PROJECT_NAME}")
    print(f"Coluna alvo: {coluna_alvo}")
    print(f"Tipo: {tipo_problema}")
    print(f"Metrica principal: {METRICA_PRINCIPAL}")
    print(f"{'='*80}\n")
    
    # ETAPA 1: Upload de dados brutos
    dataset_bruto_id, shape_bruto = component_upload_dados_brutos(
        caminho_csv=caminho_csv
    )
    
    # ETAPA 2: Pipeline de processamento
    dataset_processado_id, metricas_proc = component_pipeline_processamento(
        dataset_bruto_id=dataset_bruto_id
    )
    
    # ETAPA 3: Pipeline de features
    dataset_features_id, artefatos_feat = component_pipeline_features(
        dataset_processado_id=dataset_processado_id
    )
    
    # ETAPA 4: Pipeline de treinamento
    resultado_treino, caminho_modelo = component_pipeline_treinamento(
        dataset_features_id=dataset_features_id,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        n_modelos=n_modelos,
        otimizar=otimizar,
        n_iter=n_iter
    )
    
    # ETAPA 5: Registro do modelo
    model_id = component_registrar_modelo(
        resultado_treinamento=resultado_treino,
        caminho_modelo=caminho_modelo,
        dataset_features_id=dataset_features_id
    )
    
    # Resumo final
    resumo = {
        "projeto": PROJECT_NAME,
        "datasets": {
            "bruto": dataset_bruto_id,
            "processado": dataset_processado_id,
            "features": dataset_features_id
        },
        "modelo": {
            "id": model_id,
            "nome": resultado_treino['melhor_modelo'],
            "metrica_principal": METRICA_PRINCIPAL,
            "valor": resultado_treino['valor_metrica_principal']
        },
        "shape_bruto": shape_bruto,
        "metricas_processamento": metricas_proc,
        "artefatos_features": artefatos_feat
    }
    
    print(f"\n{'='*80}")
    print(f"PIPELINE COMPLETO FINALIZADO!")
    print(f"{'='*80}")
    print(f"\nResumo:")
    print(f"  - Datasets criados: 3 (bruto, processado, features)")
    print(f"  - Modelo: {resultado_treino['melhor_modelo']}")
    print(f"  - {METRICA_PRINCIPAL}: {resultado_treino['valor_metrica_principal']:.4f}")
    print(f"\nTodos os recursos registrados no projeto '{PROJECT_NAME}'")
    print(f"{'='*80}\n")
    
    return resumo


# ============================================================================
# FUNcaO AUXILIAR PARA EXECUcaO
# ============================================================================
def executar_pipeline(
    caminho_csv: str,
    run_locally: bool = True,
    queue_name: str = None
) -> Dict[str, Any]:
    """
    Executa o pipeline completo.
    
    Args:
        caminho_csv: Caminho para arquivo CSV
        run_locally: Se True, executa localmente; se False, envia para fila
        queue_name: Nome da fila para execucao remota (se run_locally=False)
        
    Returns:
        Resultado do pipeline
    """
    # Configurar execucao
    if run_locally:
        PipelineDecorator.run_locally()
        print("Modo: EXECUCAO LOCAL")
    else:
        if queue_name:
            PipelineDecorator.set_default_execution_queue(queue_name)
            print(f"Modo: EXECUCAO REMOTA (fila: {queue_name})")
        else:
            print("AVISO: Execucao remota sem fila definida")
    
    # Executar pipeline
    resultado = pipeline_completo_clearml(
        caminho_csv=caminho_csv,
        coluna_alvo=COLUNA_ALVO,
        tipo_problema=TIPO_PROBLEMA,
        n_modelos=3,
        otimizar=True,
        n_iter=10
    )
    
    return resultado


# ============================================================================
# MAIN (para teste direto)
# ============================================================================
if __name__ == "__main__":
    # Caminho dos dados (ajustar conforme necessario)
    CAMINHO_DADOS = "../dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv"
    
    # Executar localmente
    resultado = executar_pipeline(
        caminho_csv=CAMINHO_DADOS,
        run_locally=True
    )
    
    print("\n" + "="*80)
    print("RESULTADO FINAL:")
    print("="*80)
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")

