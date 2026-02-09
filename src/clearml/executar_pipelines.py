"""
Orquestrador de Pipelines Independentes
========================================

Executa os 3 pipelines em sequencia, passando os IDs entre eles.
Ou execute cada pipeline separadamente conforme necessidade.
"""

from pathlib import Path
from typing import Dict, Any

from src.clearml.pipeline_01_processamento import pipeline_processamento_dados
from src.clearml.pipeline_02_features import pipeline_features
from src.clearml.pipeline_03_treinamento import pipeline_treinamento


def executar_pipelines_completo(
    caminho_csv: str,
    coluna_alvo: str = "p1",
    tipo_problema: str = "regressao",
    n_modelos: int = 3,
    otimizar: bool = True,
    n_iter: int = 10,
    project_name: str = None
) -> Dict[str, Any]:
    """
    Executa os 3 pipelines em sequencia.
    
    Args:
        caminho_csv: Caminho para arquivo CSV de dados brutos
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos: Numero de modelos para comparar
        otimizar: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes de otimizacao
        project_name: Nome do projeto ClearML (cria se nao existir)
        
    Returns:
        dict com todos os IDs e resultados
    """
    proj_name = project_name or "conforto_termico"
    
    print("\n" + "="*80)
    print("EXECUTANDO PIPELINES COMPLETOS")
    print("="*80)
    print(f"Projeto ClearML: {proj_name}")
    print("="*80 + "\n")
    
    # Pipeline 1: Processamento
    print("\n>>> INICIANDO PIPELINE 1: PROCESSAMENTO")
    resultado_1 = pipeline_processamento_dados(
        caminho_csv=caminho_csv,
        criar_dataset_bruto=True,
        project_name=proj_name
    )
    dataset_processado_id = resultado_1['dataset_processado_id']
    print(f">>> Dataset processado: {dataset_processado_id}\n")
    
    # Pipeline 2: Features
    print("\n>>> INICIANDO PIPELINE 2: FEATURES")
    resultado_2 = pipeline_features(
        dataset_processado_id=dataset_processado_id,
        project_name=proj_name
    )
    dataset_features_id = resultado_2['dataset_features_id']
    print(f">>> Dataset features: {dataset_features_id}\n")
    
    # Pipeline 3: Treinamento
    print("\n>>> INICIANDO PIPELINE 3: TREINAMENTO")
    resultado_3 = pipeline_treinamento(
        dataset_features_id=dataset_features_id,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        n_modelos=n_modelos,
        otimizar=otimizar,
        n_iter=n_iter,
        project_name=proj_name
    )
    print(f">>> Modelo: {resultado_3['model_id']}\n")
    
    # Resumo final
    resumo = {
        "project_name": proj_name,
        "pipeline_1": resultado_1,
        "pipeline_2": resultado_2,
        "pipeline_3": resultado_3,
        "datasets": {
            "bruto": resultado_1.get('dataset_bruto_id'),
            "processado": dataset_processado_id,
            "features": dataset_features_id
        },
        "modelo": {
            "id": resultado_3['model_id'],
            "nome": resultado_3['melhor_modelo'],
            "metricas": resultado_3['metricas']
        }
    }
    
    print("\n" + "="*80)
    print("TODOS OS PIPELINES CONCLUIDOS!")
    print("="*80)
    print(f"\nDatasets criados:")
    print(f"  1. Bruto:      {resultado_1.get('dataset_bruto_id')}")
    print(f"  2. Processado: {dataset_processado_id}")
    print(f"  3. Features:   {dataset_features_id}")
    print(f"\nModelo:")
    print(f"  - ID:   {resultado_3['model_id']}")
    print(f"  - Nome: {resultado_3['melhor_modelo']}")
    print(f"  - R2:   {resultado_3['metricas'].get('R2', 0):.4f}")
    print("\n" + "="*80 + "\n")
    
    return resumo


if __name__ == "__main__":
    # Executar pipelines completos
    resultado = executar_pipelines_completo(
        caminho_csv="dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv",
        coluna_alvo="p1",
        tipo_problema="regressao",
        n_modelos=3,
        otimizar=True,
        n_iter=10,
        project_name="conforto_termico"  # Ou None para usar default
    )
    
    print(f"\n\nRESUMO FINAL:")
    print(f"Dataset features: {resultado['datasets']['features']}")
    print(f"Modelo: {resultado['modelo']['nome']}")
    print(f"Model ID: {resultado['modelo']['id']}")
