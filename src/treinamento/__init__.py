"""Interface pública do módulo de treinamento."""

from config.config_gerais import METRICAS_CLASSIFICACAO, PARAMS_PADRAO, PYCARET_PLOTS
from config.logger_config import logger

from .configuracao import (
    criar_experimento_classificacao,
    configurar_parametros,
    validar_parametros,
    parametros_rapidos,
)

from .treino import (
    finalizar_modelo,
    otimizar_modelo,
    treinar_modelo_base,
)

from .avaliacao import avaliar_modelo, classificar_metricas, fazer_predicoes

from .persistencia import carregar_modelo, salvar_modelo

from .visualizacao import salvar_plots_modelo

from .utils import (
    extrair_estimador,
    extrair_importancia_features,
    extrair_info_modelo,
)

__all__ = [
    "PYCARET_PLOTS",
    "METRICAS_CLASSIFICACAO",
    "PARAMS_PADRAO",
    "logger",
    "criar_experimento_classificacao",
    "configurar_parametros",
    "validar_parametros",
    "parametros_rapidos",
    "treinar_modelo_base",
    "otimizar_modelo",
    "finalizar_modelo",
    "avaliar_modelo",
    "classificar_metricas",
    "fazer_predicoes",
    "salvar_modelo",
    "carregar_modelo",
    "salvar_plots_modelo",
    "extrair_estimador",
    "extrair_info_modelo",
    "extrair_importancia_features",
]
