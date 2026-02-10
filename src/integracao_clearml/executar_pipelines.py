"""
Orquestrador de pipelines ClearML.

Executa processamento -> features -> treinamento em sequencia.
Permite execucao local (offline) sem depender de servidor ClearML.
"""

from typing import Any, Dict, Optional

from src.integracao_clearml.pipelines_clearml import (
    executar_pipeline_features_clearml,
    executar_pipeline_processamento_clearml,
    executar_pipeline_treinamento_clearml,
)


def executar_pipelines_completo(
    caminho_csv: str,
    coluna_alvo: str = "p1",
    tipo_problema: str = "regressao",
    n_modelos_comparar: int = 3,
    otimizar_hiperparametros: bool = True,
    n_iter: int = 10,
    project_name: Optional[str] = None,
    offline_mode: bool = False,
) -> Dict[str, Any]:
    """
    Executa os 3 pipelines em sequencia.

    Args:
        caminho_csv: Caminho para arquivo CSV de dados brutos
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos_comparar: Numero de modelos para comparar
        otimizar_hiperparametros: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes de otimizacao
        project_name: Nome do projeto ClearML
        offline_mode: Se True, executa sem registrar no ClearML

    Returns:
        Dict com resultados e IDs entre pipelines.
    """
    proj_name = project_name or "conforto_termico"

    print("\n" + "=" * 80)
    print("EXECUTANDO PIPELINES COMPLETOS")
    print("=" * 80)
    print(f"Projeto ClearML: {proj_name}")
    print(f"Modo: {'OFFLINE' if offline_mode else 'ONLINE'}")
    print("=" * 80 + "\n")

    print("\n>>> INICIANDO PIPELINE 1: PROCESSAMENTO")
    resultado_1 = executar_pipeline_processamento_clearml(
        caminho_csv=caminho_csv,
        project_name=proj_name,
        offline_mode=offline_mode,
    )
    dataset_processado_id = resultado_1.get("dataset_id")
    df_processado = resultado_1["df_processado"]
    print(f">>> Dataset processado: {dataset_processado_id}\n")

    print("\n>>> INICIANDO PIPELINE 2: FEATURES")
    resultado_2 = executar_pipeline_features_clearml(
        df_processado=df_processado,
        dataset_processado_id=dataset_processado_id,
        project_name=proj_name,
        offline_mode=offline_mode,
    )
    dataset_features_id = resultado_2.get("dataset_id")
    df_features = resultado_2["dados_features"]
    print(f">>> Dataset features: {dataset_features_id}\n")

    print("\n>>> INICIANDO PIPELINE 3: TREINAMENTO")
    resultado_3 = executar_pipeline_treinamento_clearml(
        df_features=df_features,
        coluna_alvo=coluna_alvo,
        tipo_problema=tipo_problema,
        dataset_features_id=dataset_features_id,
        n_modelos_comparar=n_modelos_comparar,
        otimizar_hiperparametros=otimizar_hiperparametros,
        n_iter_otimizacao=n_iter,
        project_name=proj_name,
        offline_mode=offline_mode,
    )
    print(f">>> Modelo ID: {resultado_3.get('model_id')}\n")

    nome_melhor_modelo = str(resultado_3["tabela_comparacao"].index[0])
    metricas_melhor = resultado_3.get("metricas_melhor", {})

    resumo = {
        "project_name": proj_name,
        "pipeline_1": resultado_1,
        "pipeline_2": resultado_2,
        "pipeline_3": resultado_3,
        "datasets": {
            "processado": dataset_processado_id,
            "features": dataset_features_id,
        },
        "modelo": {
            "id": resultado_3.get("model_id"),
            "nome": nome_melhor_modelo,
            "metricas": metricas_melhor,
        },
    }

    print("\n" + "=" * 80)
    print("TODOS OS PIPELINES CONCLUIDOS!")
    print("=" * 80)
    print("\nDatasets criados:")
    print(f"  1. Processado: {dataset_processado_id}")
    print(f"  2. Features:   {dataset_features_id}")
    print("\nModelo:")
    print(f"  - ID:   {resultado_3.get('model_id')}")
    print(f"  - Nome: {nome_melhor_modelo}")
    print(f"  - R2:   {metricas_melhor.get('R2', 0):.4f}")
    print("\n" + "=" * 80 + "\n")

    return resumo


if __name__ == "__main__":
    resultado = executar_pipelines_completo(
        caminho_csv="dados/2025.05.14_thermal_confort_santa_maria_brazil_.csv",
        coluna_alvo="p1",
        tipo_problema="regressao",
        n_modelos_comparar=3,
        otimizar_hiperparametros=True,
        n_iter=10,
        project_name="conforto_termico",
        offline_mode=True,
    )

    print("\n\nRESUMO FINAL:")
    print(f"Dataset features: {resultado['datasets']['features']}")
    print(f"Modelo: {resultado['modelo']['nome']}")
    print(f"Model ID: {resultado['modelo']['id']}")
