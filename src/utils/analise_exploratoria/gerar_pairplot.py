"""
Gera um pairplot com configurações personalizadas.
"""
import matplotlib.pyplot as plt
import seaborn as sns


def gerar_pairplot(df, features, hue_col=None, fonte_size=10):
    """
    Gera um pairplot com configurações personalizadas.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados.
    features (list): Lista de colunas numéricas a serem plotadas.
    hue_col (str): Coluna para definir a cor dos pontos (default: "mes-ano").
    fonte_size (int): Tamanho da fonte dos eixos e legenda (default: 10).

    Retorna:
    Exibe um gráfico PairPlot personalizado.
    """
    # Criar o PairPlot
    g = sns.pairplot(df[features], hue=hue_col, diag_kind="hist")

    # Personalizar rótulos dos eixos e legendas
    for ax in g.axes.flatten():
        if ax is not None:
            ax.set_xlabel(ax.get_xlabel(), fontsize=fonte_size)
            ax.set_ylabel(ax.get_ylabel(), fontsize=fonte_size)
            ax.tick_params(
                axis="both", which="major", labelsize=fonte_size, labelcolor="black"
            )

    # Ajustar a legenda
    if hue_col != None:
        legend = g._legend
        legend.set_title(hue_col, prop={"size": fonte_size})

        for text in legend.get_texts():
            text.set_fontsize(fonte_size)

        legend.get_frame().set_edgecolor("black")
        legend.get_frame().set_linewidth(1.2)

    # Título do gráfico
    plt.suptitle("", fontsize=fonte_size * 1.5, weight="bold", y=1.02)
    plt.show()
