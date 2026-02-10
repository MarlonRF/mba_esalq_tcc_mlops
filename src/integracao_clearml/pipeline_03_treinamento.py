"""
Pipeline 3: Treinamento e Comparacao de Modelos
================================================

Pipeline independente que:
1. Carrega dados com features (do Dataset ou arquivo)
2. Treina e compara multiplos modelos
3. Registra metricas e modelo no ClearML
"""

from pathlib import Path
import pandas as pd
from typing import Dict, Any, Optional
from clearml import Task, Dataset, OutputModel

from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo
from src.utils.io.io_local import load_dataframe


PROJECT_NAME_DEFAULT = "conforto_termico"


def pipeline_treinamento(
    dataset_features_id: Optional[str] = None,
    caminho_csv: Optional[str] = None,
    coluna_alvo: str = "p1",
    tipo_problema: str = "regressao",
    n_modelos: int = 3,
    otimizar: bool = True,
    n_iter: int = 10,
    metrica_principal: str = "R2",
    project_name: str = None
) -> Dict[str, Any]:
    """
    Pipeline de treinamento de modelos com ClearML.
    
    Args:
        dataset_features_id: ID do dataset com features (prioritario)
        caminho_csv: Caminho alternativo se nao usar dataset
        coluna_alvo: Nome da coluna alvo
        tipo_problema: 'regressao' ou 'classificacao'
        n_modelos: Numero de modelos para comparar
        otimizar: Se deve otimizar hiperparametros
        n_iter: Numero de iteracoes de otimizacao
        metrica_principal: Metrica para decisao de modelo vigente
        project_name: Nome do projeto ClearML (usa default se None)
        
    Returns:
        dict com model_id, metricas e informacoes do treinamento
    """
    # Definir projeto
    proj_name = project_name or PROJECT_NAME_DEFAULT
    
    # Criar task
    task = Task.init(
        project_name=proj_name,
        task_name="Pipeline_03_Treinamento",
        task_type=Task.TaskTypes.training,
        reuse_last_task_id=False,
        auto_connect_frameworks=False
    )
    
    task.connect_configuration({
        "dataset_features_id": dataset_features_id,
        "caminho_csv": caminho_csv,
        "coluna_alvo": coluna_alvo,
        "tipo_problema": tipo_problema,
        "n_modelos": n_modelos,
        "otimizar": otimizar,
        "n_iter": n_iter,
        "metrica_principal": metrica_principal
    })
    logger = task.get_logger()
    
    print("="*80)
    print("PIPELINE 3: TREINAMENTO DE MODELOS")
    print("="*80)
    
    try:
        # Carregar dados
        if dataset_features_id:
            print(f"\n[1] Baixando Dataset: {dataset_features_id}")
            dataset = Dataset.get(dataset_id=dataset_features_id)
            local_path = dataset.get_local_copy()
            csv_files = list(Path(local_path).glob("*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"Nenhum CSV encontrado em {local_path}")
            df_features = load_dataframe(str(csv_files[0]))
        elif caminho_csv:
            print(f"\n[1] Carregando arquivo: {caminho_csv}")
            caminho_absoluto = Path(caminho_csv).resolve()
            if not caminho_absoluto.exists():
                caminho_absoluto = Path(__file__).parent.parent.parent / caminho_csv
            df_features = load_dataframe(str(caminho_absoluto))
        else:
            raise ValueError("Forneca dataset_features_id OU caminho_csv")
        
        print(f"    Shape: {df_features.shape}")
        
        # Preparar dados
        print(f"\n[2] Preparando dados para treino...")
        print(f"    Coluna alvo: {coluna_alvo}")
        df_treino = df_features.dropna()
        print(f"    Shape final: {df_treino.shape}")
        
        logger.report_single_value("dados_treino_linhas", df_treino.shape[0])
        logger.report_single_value("dados_treino_features", df_treino.shape[1] - 1)
        
        # Treinamento
        print(f"\n[3] Treinando modelos...")
        print(f"    Tipo: {tipo_problema}")
        print(f"    Modelos a comparar: {n_modelos}")
        print(f"    Otimizacao: {'Sim' if otimizar else 'Nao'}")
        
        resultado = treinar_pipeline_completo(
            dados=df_treino,
            coluna_alvo=coluna_alvo,
            tipo_problema=tipo_problema,
            n_modelos_comparar=n_modelos,
            otimizar_hiperparametros=otimizar,
            n_iter_otimizacao=n_iter,
            salvar_modelo_final=True,
            nome_modelo="modelo_clearml",
            pasta_modelos="../modelos"
        )
        
        # Registrar metricas
        print(f"\n[4] Registrando metricas...")
        metricas = resultado['metricas_melhor']
        for nome, valor in metricas.items():
            if isinstance(valor, (int, float)):
                logger.report_single_value(nome, valor)
                print(f"    {nome}: {valor:.4f}")
        
        # Upload tabela comparacao
        tabela_comparacao = resultado['tabela_comparacao']
        task.upload_artifact("comparacao_modelos", artifact_object=tabela_comparacao)
        
        # Grafico de comparacao
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colunas_plot = ['MAE', 'MSE', 'RMSE', 'R2'] if tipo_problema == 'regressao' else ['Accuracy', 'AUC', 'Recall', 'Prec.', 'F1']
        colunas_disponiveis = [col for col in colunas_plot if col in tabela_comparacao.columns]
        
        if colunas_disponiveis:
            tabela_comparacao[colunas_disponiveis].plot(kind='bar', ax=ax)
            ax.set_title('Comparacao de Modelos')
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
        
        # Registro do modelo
        print(f"\n[5] Registrando modelo...")
        melhor_modelo_nome = str(tabela_comparacao.index[0])
        
        output_model = OutputModel(
            task=task,
            name=f"modelo_{melhor_modelo_nome}",
            framework="PyCaret"
        )
        
        output_model.update_labels({
            "tipo": tipo_problema,
            "coluna_alvo": coluna_alvo,
            "melhor_modelo": melhor_modelo_nome,
            metrica_principal: str(metricas.get(metrica_principal, 0))
        })
        
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
                print(f"    Arquivo: {caminho_modelo.name}")
        
        # Tags
        task.add_tags([
            tipo_problema,
            melhor_modelo_nome,
            f"{metrica_principal}_{metricas.get(metrica_principal, 0):.2f}".replace(".", "_")
        ])
        
        # Resumo
        resultado_final = {
            "task_id": task.id,
            "model_id": output_model.id if output_model else None,
            "melhor_modelo": melhor_modelo_nome,
            "metricas": {k: float(v) for k, v in metricas.items() 
                        if isinstance(v, (int, float))},
            "n_samples": df_treino.shape[0],
            "n_features": df_treino.shape[1] - 1
        }
        
        print("\n" + "="*80)
        print("PIPELINE 3 CONCLUIDO!")
        print("="*80)
        print(f"Melhor modelo: {melhor_modelo_nome}")
        print(f"{metrica_principal}: {metricas.get(metrica_principal, 0):.4f}")
        print(f"Model ID: {output_model.id if output_model else 'N/A'}")
        print("="*80)
        
        task.close()
        return resultado_final
        
    except Exception as e:
        task.mark_failed(status_message=str(e))
        task.close()
        raise


if __name__ == "__main__":
    # Exemplo de uso com dataset
    resultado = pipeline_treinamento(
        dataset_features_id="COLE_AQUI_O_ID_DO_DATASET_FEATURES",
        coluna_alvo="p1",
        tipo_problema="regressao",
        n_modelos=3,
        otimizar=True,
        n_iter=10
    )
    print(f"\nResultado: {resultado}")
