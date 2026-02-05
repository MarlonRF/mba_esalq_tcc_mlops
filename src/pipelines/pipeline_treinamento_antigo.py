# Importações organizadas por ordem alfabética
import logging
import os
import shutil

import pandas as pd
from clearml import Logger, OutputModel, Task
from clearml.automation import PipelineDecorator
from pycaret.classification import (ClassificationExperiment, compare_models,
                                    finalize_model, save_model, setup,
                                    tune_model)

# ------------------------------------------------------------------------------------------
#                                         FUNÇÕES AUXILIARES
# ------------------------------------------------------------------------------------------



def salvar_plots_modelo_custom(
    exp: ClassificationExperiment,
    modelos: list,
    plots: list,
    pasta: str = "graficos",
    scale: float = 1.5,
    add_prefix: bool = True,
):
    """
    Gera e salva gráficos customizados de modelos do PyCaret com opções avançadas.

    Args:
        exp (ClassificationExperiment): O objeto do experimento do PyCaret.
        modelos (list): Uma lista de modelos treinados.
        plots (list): Uma lista com os nomes dos plots a serem gerados.
        pasta (str): A pasta de destino para salvar os gráficos. Default: "graficos"
        scale (float): A escala de resolução do gráfico (ex: 1.5, 2). Default: 1.5
        add_prefix (bool): Se True, adiciona o nome do modelo como prefixo no arquivo. Default: True

    Returns:
        dict: Um dicionário com os nomes dos modelos como chaves e outro dicionário
              com os nomes dos plots e seus caminhos de arquivo como valores.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    os.makedirs(pasta, exist_ok=True)

    resultados_gerais = {}

    for modelo in modelos:
        try:
            nome_modelo = modelo.get_params()["__meta__"]["Name"]
        except (AttributeError, KeyError):
            nome_modelo = modelo.__class__.__name__

        logging.info(f"Gerando plots para o modelo: '{nome_modelo}'")

        caminhos_plots = {}
        for tipo_plot in plots:
            try:
                # Usa o parâmetro 'scale' para aumentar a resolução
                caminho_original = exp.plot_model(
                    modelo, plot=tipo_plot, save=True, verbose=False, scale=scale
                )

                nome_arquivo_original = os.path.basename(caminho_original)

                # LÓGICA PARA ADICIONAR O PREFIXO
                if add_prefix:
                    prefixo = nome_modelo.replace(
                        " ", "_"
                    )  # Ex: 'Gradient Boosting Classifier' -> 'Gradient_Boosting_Classifier'
                    nome_arquivo_final = f"{prefixo}_{nome_arquivo_original}"
                else:
                    nome_arquivo_final = nome_arquivo_original

                caminho_destino = os.path.join(pasta, nome_arquivo_final)

                shutil.move(caminho_original, caminho_destino)
                caminhos_plots[tipo_plot] = caminho_destino
                logging.info(f"--> Plot '{tipo_plot}' salvo em: {caminho_destino}")

            except Exception as e:
                caminhos_plots[tipo_plot] = f"Erro ao gerar plot '{tipo_plot}'"
                logging.error(
                    f"Falha ao gerar o plot '{tipo_plot}' para {nome_modelo}: {e}"
                )

        resultados_gerais[nome_modelo] = caminhos_plots

    return resultados_gerais


PipelineDecorator.component(return_values=["tabela_classificada"])


def classificarMetricas(tabela, metricas):
    """
    Classifica modelos baseado em múltiplas métricas e calcula uma classificação média.

    Args:
        tabela (pd.DataFrame): DataFrame contendo as métricas dos modelos
        metricas (list): Lista das métricas a serem utilizadas para classificação

    Returns:
        pd.DataFrame: Tabela com colunas adicionais de classificação para cada métrica
                     e uma coluna de classificação média
    """
    for metrica in metricas:
        tabela[f"classificacao_{metrica}"] = (
            tabela[metrica].rank(ascending=False, method="min").astype(int)
        )
    tabela["classificacao_media"] = tabela[
        [f"classificacao_{m}" for m in metricas]
    ].mean(axis=1)
    return tabela


PipelineDecorator.component(return_values=["estimador"])


def extrair_estimador(modelo_pipeline):
    """
    Extrai o estimador principal de um pipeline do PyCaret.

    Args:
        modelo_pipeline: Pipeline ou modelo do PyCaret

    Returns:
        O estimador/modelo subjacente
    """
    # Em PyCaret o estimador costuma estar em 'trained_model'; se não, pega o último passo
    steps = getattr(modelo_pipeline, "named_steps", None)
    if steps:
        estimador = steps.get("trained_model", list(steps.values())[-1])
    else:
        estimador = modelo_pipeline
    return estimador


PipelineDecorator.component(return_values=["info_modelo"])


def extrair_info_modelo(modelo):
    """
    Extrai informações básicas de um modelo (nome e parâmetros).

    Args:
        modelo: Modelo ou pipeline do qual extrair informações

    Returns:
        dict: Dicionário com 'modelo_nome' e 'parametros'
    """
    estimador = extrair_estimador(modelo)
    nome = estimador.__class__.__name__
    try:
        parametros = estimador.get_params(deep=False)
    except Exception:
        parametros = {}
    return {
        "modelo_nome": nome,
        "parametros": parametros,
    }


PipelineDecorator.component(return_values=["resultados_gerais"])


def salvar_plots_modelo(
    exp: ClassificationExperiment, modelos: list, plots: list, pasta: str = "graficos"
):
    """
    Gera e salva gráficos de avaliação de modelos do PyCaret em uma pasta específica.

    Args:
        exp (ClassificationExperiment): O objeto do experimento do PyCaret (após o setup).
        modelos (list): Uma lista de modelos treinados para gerar os plots.
        plots (list): Uma lista de strings com os nomes dos plots a serem gerados.
        pasta (str): O nome da pasta de destino para salvar os gráficos.

    Returns:
        dict: Um dicionário com os nomes dos modelos como chaves e outro dicionário
              com os nomes dos plots e seus caminhos de arquivo como valores.
    """
    # Configuração básica de logging para acompanhar o processo
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Garante que o diretório de destino exista
    os.makedirs(pasta, exist_ok=True)

    resultados_gerais = {}

    for modelo in modelos:
        # Pega o nome do modelo a partir do objeto
        try:
            # Em versões mais recentes do PyCaret, o nome está no metadado
            nome_modelo = modelo.get_params()["__meta__"]["Name"]
        except (AttributeError, KeyError):
            # Plano B: Pega o nome da classe
            nome_modelo = modelo.__class__.__name__

        logging.info(f"Gerando plots para o modelo: '{nome_modelo}'")

        caminhos_plots = {}
        for tipo_plot in plots:
            try:
                # A função plot_model RETORNA o caminho do arquivo quando save=True
                caminho_original = exp.plot_model(
                    modelo, plot=tipo_plot, save=True, verbose=False
                )

                # Define o novo caminho na pasta de destino
                nome_arquivo = os.path.basename(caminho_original)
                caminho_destino = os.path.join(pasta, nome_arquivo)

                # Move o arquivo e armazena o novo caminho
                shutil.move(caminho_original, caminho_destino)
                caminhos_plots[tipo_plot] = caminho_destino
                logging.info(f"--> Plot '{tipo_plot}' salvo em: {caminho_destino}")

            except Exception as e:
                caminhos_plots[tipo_plot] = f"Erro ao gerar plot '{tipo_plot}'"
                logging.error(
                    f"Falha ao gerar o plot '{tipo_plot}' para o modelo {nome_modelo}: {e}"
                )

        resultados_gerais[nome_modelo] = caminhos_plots

    return resultados_gerais


PipelineDecorator.component(return_values=["exp", "modelo_tunado", "resultado"])


def treinar_classificacao(params: dict):
    """
    Executa um pipeline completo de treinamento de classificação usando PyCaret.

    Args:
        params (dict): Parâmetros de configuração para o experimento PyCaret

    Returns:
        tuple: (experimento, modelo_tunado, resultado)
            - experimento: Objeto ClassificationExperiment configurado
            - modelo_tunado: Melhor modelo após tunagem de hiperparâmetros
            - resultado: Dicionário com tabelas, métricas e gráficos
    """
    exp = ClassificationExperiment()
    exp.setup(**params)

    resultado = {"tabelas": {}, "metricas": {}, "graficos": {}}

    best_model = exp.compare_models(verbose=False)
    resultado["tabelas"]["comparacao_modelos"] = exp.pull().copy()

    modelo_tunado = exp.tune_model(best_model, verbose=False)
    resultado["tabelas"]["modelo_otimizado"] = exp.pull().copy()

    predicoes = exp.predict_model(modelo_tunado)
    resultado["tabelas"]["predicoes_modelo"] = predicoes.copy()
    resultado["metricas"]["metricas_modelo"] = exp.pull().copy()
    modelo_final = exp.finalize_model(modelo_tunado)
    exp.create_api(modelo_final, "api")

    return exp, modelo_tunado, resultado


PipelineDecorator.component(return_values=["informacoes_gerais_exp"])


def info_experimento_e_modelo(
    exp, modelo_tunado, resultado, coluna_alvo, atributos, params
):
    # -------------------------------------
    # Extração de informações do modelo
    # -------------------------------------
    print("Extração de informações do modelo")
    estimador = extrair_estimador(modelo_tunado)
    info_modelo = extrair_info_modelo(estimador)
    nome_modelo = info_modelo["modelo_nome"]
    parametros_modelo = info_modelo["parametros"]
    metricas_modelo = resultado["metricas"]["metricas_modelo"]
    tab_valid_cruzada_modl_tunado = resultado["tabelas"]["modelo_otimizado"]
    tab_predicoes = resultado["tabelas"]["predicoes_modelo"]

    try:
        parametros = exp.get_params(deep=False)  # evita expansão profunda desnecessária
    except Exception:
        parametros = {}

    informacoes_gerais_exp = {
        "Varável Alvo": coluna_alvo,
        "Atributos": atributos,
        "modelo_nome": nome_modelo,
        "Parametros de configuração do Experimento": params,
        "Parametros do modelo": parametros,
        "Metricas do modelo": metricas_modelo.to_dict(orient="records"),
    }

    # ------------------------------------------------------------------------------------------
    #                 SALVANDO O MODELO TREINADO COM DATA E HORA NO NOME
    # ------------------------------------------------------------------------------------------

    import datetime as timnow

    # Save the trained model
    data = timnow.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    from pathlib import Path

    # ------------------------------------------------------------------------------------------
    #                 SALVANDO O MODELO TREINADO COM FALLBACKS PARA PERMISSÕES
    # ------------------------------------------------------------------------------------------
    
    import tempfile
    import shutil
    
    # Tentar criar diretório modelos com permissões adequadas
    try:
        pasta_modelo = Path("modelos")
        os.makedirs("modelos", mode=0o755, exist_ok=True)
        caminho_modelo = f"modelos/{nome_modelo}_{data}"
        use_temp_dir = False
    except (PermissionError, OSError) as e:
        print(f"⚠️ Não foi possível criar diretório modelos: {e}")
        print(">> Usando diretório temporário como fallback...")
        temp_dir = tempfile.mkdtemp()
        pasta_modelo = Path(temp_dir)
        caminho_modelo = f"{temp_dir}/{nome_modelo}_{data}"
        use_temp_dir = True

    # Tentar salvar o modelo
    try:
        exp.save_model(modelo_tunado, caminho_modelo)
        print(f"✅ Modelo salvo em: {caminho_modelo}.pkl")
        
        # Se usou diretório temporário, tentar copiar para local acessível
        if use_temp_dir:
            try:
                # Tentar copiar para pasta api/
                os.makedirs("api", mode=0o755, exist_ok=True)
                shutil.copy2(f"{caminho_modelo}.pkl", "api/api.pkl")
                print(f"✅ Modelo copiado para api/api.pkl")
                caminho_completo_modelo = "api/api.pkl"
            except (PermissionError, OSError):
                # Fallback final - salvar na raiz
                shutil.copy2(f"{caminho_modelo}.pkl", "api.pkl")
                print(f"✅ Modelo salvo como api.pkl (fallback)")
                caminho_completo_modelo = "api.pkl"
        else:
            # Copiar também para a pasta api para uso posterior
            try:
                os.makedirs("api", mode=0o755, exist_ok=True)
                shutil.copy2(f"{caminho_modelo}.pkl", "api/api.pkl")
                print(f"✅ Modelo copiado para api/api.pkl")
            except (PermissionError, OSError) as e:
                print(f"⚠️ Não foi possível copiar para api/: {e}")
            caminho_completo_modelo = f"modelos/{nome_modelo}_{data}.pkl"
                
    except (PermissionError, OSError) as e:
        print(f"❌ Erro ao salvar modelo: {e}")
        # Último fallback - salvar diretamente na raiz
        try:
            exp.save_model(modelo_tunado, "api")
            print(f"✅ Modelo salvo como api.pkl (último fallback)")
            caminho_completo_modelo = "api.pkl"
        except Exception as e2:
            print(f"❌ Erro no último fallback: {e2}")
            raise e
    task = Task.current_task()

    if task is None:
        task = Task.init(
            project_name="conforto_termico", task_name="Pipeline de Treinamento"
        )

    # ------------------------------------------------------------------------------------------
    #                 REGISTRANDO O MODELO NO CLEARML
    # ------------------------------------------------------------------------------------------

    om = OutputModel(
        task=task,
        name="modelo_treinado_tunado",
        framework="Scikit-learn",
        tags=["pycaret", "classificação", nome_modelo],
        comment=str(informacoes_gerais_exp),
    )
    om.update_weights(caminho_completo_modelo)

    # ------------------------------------------------------------------------------------------
    #                 INFORMAÇÕES SOBRE OS MODELOS E MODELO SELECIONADO
    # ------------------------------------------------------------------------------------------
    tabela_metricas_modelos = classificarMetricas(
        resultado["tabelas"]["comparacao_modelos"],
        ["Accuracy", "AUC", "Recall", "Prec.", "F1", "Kappa", "MCC"],
    )

    dict_modelos_treinados = tabela_metricas_modelos["Model"].to_dict()

    # list_plots = list(dict_pycaret_plots.keys())
    list_plots = ["pipeline", "auc", "threshold", "pr"]
    list_modelos = list(dict_modelos_treinados.keys())
    plots = False
    if plots:
        list_plots = ["pipeline", "auc", "threshold", "pr"]
        list_modelos = list(dict_modelos_treinados.keys())
        resultados = salvar_plots_modelo(
            exp=exp,
            modelos=[modelo_tunado],
            plots=list_plots,  # ['pipeline', 'auc', 'threshold', 'pr'],
            pasta="graficos_gbc",
        )

    # ------------------------------------------------------------------------------------------
    #                                         REGISTRO DAS INFORMAÇÕES NO CLEARML
    # ------------------------------------------------------------------------------------------
    Logger.current_logger().report_table(
        title="tabela_metricas_modelos",  # Título do gráfico/tabela
        series="Bla",  # Nome da série (para agrupar gráficos)
        iteration=0,  # Iteração (útil para registrar ao longo do tempo)
        table_plot=tabela_metricas_modelos,  # O DataFrame a ser plotado
    )
    Logger.current_logger().report_table(
        title="tab_valid_cruzada_modl_tunado",  # Título do gráfico/tabela
        series="Bla",  # Nome da série (para agrupar gráficos)
        iteration=0,  # Iteração (útil para registrar ao longo do tempo)
        table_plot=tab_valid_cruzada_modl_tunado,  # O DataFrame a ser plotado
    )

    task.connect(informacoes_gerais_exp)

    task.add_tags([nome_modelo, "pycaret", "classificação"])
    task.close()


# ------------------------------------------------------------------------------------------
#                                         Treinamento
# ------------------------------------------------------------------------------------------


@PipelineDecorator.pipeline(
    name="Pipeline treinamento", project="Teste IA", version="1.0"
)
def pipeline_treinamento(atributos, coluna_alvo, params: dict):
    """
    Pipeline de treinamento de classificação com PyCaret.

    Args:
        atributos (list): Atributos utilizados para o treinamento
        coluna_alvo (str): Nome da coluna alvo (variável dependente)
        params (dict): Parâmetros adicionais para o setup

    Returns:
        ClassificationExperiment, Any, Dict: Experimento configurado, modelo selecionado e resultado do treinamento
    """
    exp, modelo_selecionado, resultado = treinar_classificacao(params)
    info_experimento_e_modelo(
        exp, modelo_selecionado, resultado, coluna_alvo, atributos, params
    )


if __name__ == "__main__":
    # Inicia uma tarefa ClearML

    # Carrega os dados (substitua pelo seu método de carregamento)
    df = pd.read_csv("dados_brutos.csv")

    # Executa o pipeline de processamento
    df_processado = pipeline_treinamento(df=df)

    # Salva o DataFrame processado
    df_processado.to_csv("dados_processados.csv", index=False)

    print("Processamento concluído e dados salvos em 'dados_processados.csv'")
