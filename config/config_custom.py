"""
Configurações personalizadas do projeto específico: conjunto de dados, 
dicionários de nomes de variáveis, etc.
"""
import numpy as np

NOME_PROJETO = "Estudo de Sensação Térmica Humana em Santa Maria - RS"


SUBSTITUICOES_LIMPEZA = {
    "NAN": np.nan,
    "nan": np.nan,
    "": np.nan,
    "-": np.nan,
    "x": np.nan,
    "99": np.nan,
    "F": "f",
}

# Conversao de tipos (data, hora, numericos, categoricos)
TYPE_DICT = {
    "data": "datetime64[ns]",
    "hora": "datetime64[ns]",
    "idade": "Int64",
    "sexo": "string",
    "peso": "Int64",
    "altura": "float64",
    "vestimenta": "string",
    "p1": "Int64",
    "p2": "Int64",
    "p3": "Int64",
    "p4": "Int64",
    "p5": "Int64",
    "p6": "Int64",
    "p7": "Int64",
    "p8": "Int64",
    "tev": "float64",
    "utci": "float64",
    "sst": "float64",
    "ste": "float64",
    "psti": "float64",
    "wbgt": "float64",
    "wci": "float64",
    "tek": "float64",
    "te": "float64",
    "pst": "float64",
    "tmedia": "float64",
    "tmax": "float64",
    "tmin": "float64",
    "tu": "float64",
    "ur": "float64",
    "ur_max": "float64",
    "ur_min": "float64",
    "rsolarmed": "float64",
    "rsolartot": "float64",
    "vel_vento": "float64",
    "dir_vento": "float64",
    "sd_dirvento": "float64",
    "vel_vento_max": "float64",
    "dir_max_vento": "float64",
    "chuva_tot": "float64",
}

COLUNA_DATA = "data"
COLUNA_HORA = "hora"

COLUNAS_PONTO_FLUTUANTE = [
    "tmedia",
    "tmax",
    "tmin",
    "ur",
    "ur_max",
    "ur_min",
    "rsolarmed",
    "rsolartot",
    "vel_vento",
    "sd_dirvento",
    "vel_vento_max",
    "chuva_tot",
    "altura",
    "peso",
    "tu",
]

COLUNAS_NUMEROS_INTEIROS = [
    "idade",
    "p1",
    "p2",
    "p3",
    "p4",
    "p5",
    "p6",
    "p7",
    "p8",
]

COLUNAS_CATEGORICAS = [
    "sexo",
    "vestimenta",
]

TIPOS_FEATURES_DERIVADAS = [
    "imc",
    "imc_classe",
    "heat_index",
    "dew_point",
    "t*u",
    "t/u",
]

METODO_IMPUTACAO_NUM = "median"
METODO_IMPUTACAO_CAT = "mode"
VALOR_CONST_CATEGORICA = "__missing__"

# Configuração avançada de imputação por coluna (compatível com pipeline antigo)
CONFIG_IMPUTACAO_CUSTOMIZADA = {
    # Perguntas do questionário: backward fill (como no pipeline antigo)
    "p5": "backward",
    "p6": "backward",
    "p7": "backward",
    "p8": "backward",
    
    # Vestimenta: backward fill
    "vestimenta": "backward",
    
    # Variáveis meteorológicas: usar média móvel + interpolação
    # (tratamento especial no pipeline via imputar_media_movel_interpolada)
    "rsolartot": "rolling_mean_48",  # Indicador especial
    "rsolarmed": "rolling_mean_48",  # Indicador especial
    
    # Demográficas: mediana
    "idade": "median",
    "peso": "median",
    "altura": "median",
    
    # Outras categóricas: mode
    "sexo": "mode",
    
    # tu: será calculado via features derivadas se faltante
}

CRIAR_FEATURES_TEMPORAIS = True
CRIAR_COLUNA_MES_ANO = True

APLICAR_CODIFICACAO = True
METODO_CODIFICACAO = "label"  # label|onehot
SUFIXO_CODIFICADAS = "_cod"

APLICAR_NORMALIZACAO = True
COLUNAS_NORMALIZAR = None
METODO_NORMALIZACAO = "standard"
AGRUPAMENTO_NORMALIZAR = "mes-ano"
SUFIXO_NORMALIZADAS = "_norm"

SALVAR_MAPEAMENTOS = True
DIRETORIO_ARTEFATOS = "artefatos_processamento"

# Mapeamentos de renome e alvo (simples, opcionais)
MAPA_SENSACAO_TERMICA = {
    -3: "Muito Frio",
    -2: "Frio",
    -1: "Levemente Frio",
    0: "Neutro",
    1: "Levemente Quente",
    2: "Quente",
    3: "Muito Quente",
}

NOVOS_CABECALHOS = {
    "data": "data_coleta",
    "hora": "hora_coleta",
    "idade": "idade_anos",
    "sexo": "sexo_biologico",
    "peso": "peso_kg",
    "altura": "altura_cm",
    "vestimenta": "vestimenta_clo",
    "p1": "pergunta_1",
    "p2": "pergunta_2",
    "p3": "pergunta_3",
    "p4": "pergunta_4",
    "p5": "pergunta_5",
    "p6": "pergunta_6",
    "p7": "pergunta_7",
    "p8": "pergunta_8",
    "tev": "temperatura_equivalente_verao_c",
    "utci": "utci_c",
    "sst": "temperatura_superficie_c",
    "ste": "temperatura_efetiva_c",
    "psti": "indice_stress_termico_fisiologico",
    "wbgt": "wbgt_c",
    "wci": "indice_resfriamento_vento",
    "tek": "temperatura_equivalente_k",
    "te": "temperatura_equivalente_c",
    "pst": "percentual_satisfacao_termica",
    "tmedia": "temperatura_media_c",
    "tmax": "temperatura_maxima_c",
    "tmin": "temperatura_minima_c",
    "tu": "temperatura_vento_c",
    "ur": "umidade_relativa_percent",
    "ur_max": "umidade_relativa_max_percent",
    "ur_min": "umidade_relativa_min_percent",
    "rsolarmed": "radiacao_solar_media_wm2",
    "rsolartot": "radiacao_solar_total_mj",
    "vel_vento": "velocidade_vento_ms",
    "dir_vento": "direcao_vento_graus",
    "sd_dirvento": "desvio_padrao_direcao_vento",
    "vel_vento_max": "velocidade_vento_max_ms",
    "dir_max_vento": "direcao_vento_max_graus",
    "chuva_tot": "precipitacao_total_mm",
    "mes-ano": "mes_ano",
    "data_cplt": "data_completa",
}

__all__ = [
    "SUBSTITUICOES_LIMPEZA",
    "COLUNA_DATA",
    "COLUNA_HORA",
    "COLUNAS_PONTO_FLUTUANTE",
    "COLUNAS_NUMEROS_INTEIROS",
    "COLUNAS_CATEGORICAS",
    "TIPOS_FEATURES_DERIVADAS",
    "METODO_IMPUTACAO_NUM",
    "METODO_IMPUTACAO_CAT",
    "VALOR_CONST_CATEGORICA",
    "CRIAR_FEATURES_TEMPORAIS",
    "CRIAR_COLUNA_MES_ANO",
    "APLICAR_CODIFICACAO",
    "METODO_CODIFICACAO",
    "SUFIXO_CODIFICADAS",
    "APLICAR_NORMALIZACAO",
    "COLUNAS_NORMALIZAR",
    "METODO_NORMALIZACAO",
    "AGRUPAMENTO_NORMALIZAR",
    "SUFIXO_NORMALIZADAS",
    "SALVAR_MAPEAMENTOS",
    "DIRETORIO_ARTEFATOS",
    "TYPE_DICT",
    "MAPA_SENSACAO_TERMICA",
    "RENOMEAR_COLUNAS",
]



valores_permitidos = {
    "6": [-3, -2, -1, 0, 1, 2, 3],
    "peso": [10, 131],
    "altura": [100, 200],
}
substituicoes = {99: 0, "x": 0, "F": "f"}

type_dict = {
    "data": "datetime64[ns]",  # Datas
    "hora": "datetime64[ns]",  # Horários
    "idade": "Int64",  # Idades como inteiros (com suporte a NaN)
    "sexo": "string",  # Sexo como string (categórico)
    "peso": "Int64",  # Peso como número contínuo
    "altura": "float64",  # Altura como número contínuo
    "vestimenta": "string",  # Tipo de vestimenta (categórico)
    "p1": "Int64",  # Variáveis numéricas inteiras (suporte a NaN)
    "p2": "Int64",
    "p3": "Int64",
    "p4": "Int64",
    "p5": "Int64",
    "p6": "Int64",
    "p7": "Int64",
    "p8": "Int64",
    "tev": "float64",  # Dados contínuos
    "utci": "float64",
    "sst": "float64",
    "ste": "float64",
    "psti": "float64",
    "wbgt": "float64",
    "wci": "float64",
    "tek": "float64",
    "te": "float64",
    "pst": "float64",
    "tmedia": "float64",
    "tmax": "float64",
    "tmin": "float64",
    "tu": "float64",
    "ur": "float64",  # Umidade relativa
    "ur_max": "float64",  # Umidade relativa máxima
    "ur_min": "float64",  # Umidade relativa mínima
    "rsolarmed": "float64",  # Radiação solar média
    "rsolartot": "float64",  # Radiação solar total
    "vel_vento": "float64",  # Velocidade do vento
    "dir_vento": "float64",  # Direção do vento
    "sd_dirvento": "float64",  # Desvio padrão da direção do vento
    "vel_vento_max": "float64",  # Velocidade máxima do vento
    "dir_max_vento": "float64",  # Direção máxima do vento
    "chuva_tot": "float64",  # Total de chuva
}


# SELEÇAO DAS VARIÁVEIS DE INTERESSE
features_tempo = ["data", "hora"]
features_categoricas = ["sexo"]
features_numericas = [
    "idade",
    "peso",
    "altura",
    "vestimenta",
    "tmedia",
    "tmax",
    "tmin",
    "tu",
    "ur",
    "ur_max",
    "ur_min",
    "rsolarmed",
    "rsolartot",
    "vel_vento",
    "dir_vento",
    "sd_dirvento",
    "vel_vento_max",
    "dir_max_vento",
    "chuva_tot",
]

features_perguntas = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]

features_climatologicas_relevantes = [
    "tmedia",
    "tu",
    "ur",
    "rsolarmed",
    "vel_vento",
    "chuva_tot",
]

features_entrevistatos = ["idade", "peso", "altura", "vestimenta", "sexo"]
todas = features_categoricas + features_numericas + features_tempo + features_perguntas

dict_novos_nomes_cabecalhos = {
    "data": "data_coleta",
    "hora": "hora_coleta",
    "idade": "idade_anos",
    "sexo": "sexo_biologico",
    "peso": "peso_kg",
    "altura": "altura_cm",
    "vestimenta": "vestimenta_clo",  # clo = unidade de isolamento térmico
    "p1": "pergunta_1",  # ideal renomear para o tema do questionário (ex.: sensacao_termica)
    "p2": "pergunta_2",
    "p3": "pergunta_3",
    "p4": "pergunta_4",
    "p5": "pergunta_5",
    "p6": "pergunta_6",
    "p7": "pergunta_7",
    "p8": "pergunta_8",
    "tev": "temperatura_equivalente_verao_c",
    "utci": "utci_c",  # Universal Thermal Climate Index
    "sst": "temperatura_superficie_c",
    "ste": "temperatura_efetiva_c",
    "psti": "indice_stress_termico_fisiologico",
    "wbgt": "wbgt_c",  # Wet Bulb Globe Temperature
    "wci": "indice_resfriamento_vento",
    "tek": "temperatura_equivalente_k",
    "te": "temperatura_equivalente_c",
    "pst": "percentual_satisfacao_termica",
    "tmedia": "temperatura_media_c",
    "tmax": "temperatura_maxima_c",
    "tmin": "temperatura_minima_c",
    "tu": "temperatura_vento_c",  # confirmar se é T únita ou T do vento
    "ur": "umidade_relativa_percent",
    "ur_max": "umidade_relativa_max_percent",
    "ur_min": "umidade_relativa_min_percent",
    "rsolarmed": "radiacao_solar_media_wm2",
    "rsolartot": "radiacao_solar_total_mj",
    "vel_vento": "velocidade_vento_ms",
    "dir_vento": "direcao_vento_graus",
    "sd_dirvento": "desvio_padrao_direcao_vento",
    "vel_vento_max": "velocidade_vento_max_ms",
    "dir_max_vento": "direcao_vento_max_graus",
    "chuva_tot": "precipitacao_total_mm",
    "mes-ano": "mes_ano",
    "data_cplt": "data_completa",
}


mapa_sensacao_termica = {
    -3: "Muito Frio",
    -2: "Frio",
    -1: "Levemente Frio",
    0: "Neutro",
    1: "Levemente Quente",
    2: "Quente",
    3: "Muito Quente",
}


tags_p_clearml =['conforto térmico','Santa Maria RS','sensação térmica','tcc mba esalq']