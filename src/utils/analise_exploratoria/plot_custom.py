
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
