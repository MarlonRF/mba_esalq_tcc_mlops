import os

import numpy as np
import pandas as pd
from clearml import OutputModel, Task
from clearml.automation import PipelineDecorator
from ..src.config_projeto import config



# Exemplo de uso

#PipelineDecorator.component(return_values=["df_processado"])
def processar_dados(
    df, substituicoes, type_dict, renomear_colunas=None, mapear_variavel_alvo=None
):
    # Exemplo de processamento: remover valores nulos e normalizar colunas numéricas
    """
    Processa um DataFrame com as seguintes etapas:
    1. Replacer valores nulos por valores faltantes
    2. Substituir valores nas colunas
    3. Converter colunas para o tipo correto
    4. Replacer valores nulos por valores faltantes
    5. Substituir valores nas colunas
    6. Preencher valores nulos com a média móvel
    7. Interpololar valores nulos com o método linear

    Retorna o DataFrame processado.
    """
    # cabeçalhos em minúsculas e sem espaços
    df.columns = df.columns.str.lower()
    df = df.replace(",", ".", regex=True)
    df = df.replace("NAN", np.nan)

    trocar_valores = {"x": np.nan, "99": np.nan}

    df[["p5", "p6", "p7", "p8"]] = df[["p5", "p6", "p7", "p8"]].replace(trocar_valores)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df["mes-ano"] = df.data.dt.month.astype(str) + " - " + df.data.dt.year.astype(str)

    df = df.replace(substituicoes)
    df["data_cplt"] = pd.to_datetime(
        df["data"].astype("str") + " " + df["hora"].astype("str")
    )

    df = apply_column_types(df, type_dict)

    df = df.replace("NAN", np.nan)

    df["p5"] = df["p5"].bfill()

    df["p6"] = df["p6"].bfill()

    df["p7"] = df["p7"].bfill()

    df["p8"] = df["p8"].bfill()

    df["vestimenta"] = df["vestimenta"].bfill()

    df["tu"] = df.apply(
        lambda row: (
            calcular_tu_stull(row["tmedia"], row["ur"])
            if pd.isna(row["tu"])
            else row["tu"]
        ),
        axis=1,
    )

    df["rsolartot"] = df["rsolartot"].fillna(
        df["rsolartot"].rolling(window=48, min_periods=1).mean()
    )
    df["rsolartot"] = df["rsolartot"].interpolate(method="linear")
    passo_5 = df.isna().any(axis=1).sum()

    df["rsolarmed"] = df["rsolarmed"].fillna(
        df["rsolarmed"].rolling(window=48, min_periods=1).mean()
    )
    df["rsolarmed"] = df["rsolarmed"].interpolate(method="linear")

    if mapear_variavel_alvo != None:
        df["sensacao_termica"] = df["p1"].map(mapear_variavel_alvo)

    if renomear_colunas != None:
        df = df.rename(columns=renomear_colunas)

    return df


@PipelineDecorator.pipeline(
    name="Pipeline processamento", project="Test sábado", version="1.0"
)
def pipeline_processamento(df, type_dict=type_dict, substituicoes=substituicoes):
    """
    Executa o pipeline de processamento de dados de conforto térmico

    Args:
        df (pd.DataFrame): DataFrame com os dados a serem processados
        type_dict (Dict): Dicionário com os tipos das colunas
        substituicoes (Dict): Dicionário com as substituições de valores

    Returns:
        pd.DataFrame: DataFrame processado
    """
    df_processado = processar_dados(
        df,
        type_dict=type_dict,
        substituicoes=substituicoes,
        renomear_colunas=dict_novos_nomes_cabecalhos,
        mapear_variavel_alvo=mapa_sensacao_termica,
    )
    return df_processado


if __name__ == "__main__":
    # Inicia uma tarefa ClearML
    task = Task.init(project_name="Test sábado", task_name="Pipeline de Processamento")

    # Carrega os dados (substitua pelo seu método de carregamento)
    df = pd.read_csv("dados_brutos.csv")

    # Executa o pipeline de processamento
    df_processado = pipeline_processamento(df=df)

    # Salva o DataFrame processado
    df_processado.to_csv("dados_processados.csv", index=False)

    print("Processamento concluído e dados salvos em 'dados_processados.csv'")
