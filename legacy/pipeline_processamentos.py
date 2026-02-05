"""
Orquestracao do pipeline de processamento.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd

from ..src.config_projeto import config
from ..src.features.codificacao import aplicar_codificacao_label, aplicar_one_hot
from .derivadas import adicionar_features_derivadas
from ..src.processamento import imputar_categoricos, imputar_numericos
from ..src.processamento.limpeza import (
    aplicar_substituicoes,
    converter_colunas_categoricas,
    converter_colunas_float,
    converter_colunas_int,
)
from .normalizacao import normalizar
from ..src.processamento.temporal import garantir_agrupamento_temporal, converter_colunas_temporais


@dataclass
class ConfiguracaoProcessamento:
    substituicoes_limpeza: Dict = field(
        default_factory=lambda: config.SUBSTITUICOES_LIMPEZA.copy()
    )
    coluna_data: str = config.COLUNA_DATA
    coluna_hora: str = config.COLUNA_HORA
    colunas_ponto_flutuante: List[str] = field(
        default_factory=lambda: config.COLUNAS_PONTO_FLUTUANTE.copy()
    )
    colunas_numeros_inteiros: List[str] = field(
        default_factory=lambda: config.COLUNAS_NUMEROS_INTEIROS.copy()
    )
    colunas_categoricas: List[str] = field(
        default_factory=lambda: config.COLUNAS_CATEGORICAS.copy()
    )
    metodo_imputacao_numerica: str = config.METODO_IMPUTACAO_NUM
    metodo_imputacao_categorica: str = config.METODO_IMPUTACAO_CAT
    valor_constante_categorica: str = config.VALOR_CONST_CATEGORICA
    criar_features_temporais: bool = config.CRIAR_FEATURES_TEMPORAIS
    criar_coluna_mes_ano: bool = config.CRIAR_COLUNA_MES_ANO
    criar_features_derivadas: bool = True
    tipos_features_derivadas: List[str] = field(
        default_factory=lambda: config.TIPOS_FEATURES_DERIVADAS.copy()
    )
    aplicar_codificacao: bool = config.APLICAR_CODIFICACAO
    metodo_codificacao: str = config.METODO_CODIFICACAO  # label|onehot
    sufixo_colunas_codificadas: str = config.SUFIXO_CODIFICADAS
    aplicar_normalizacao: bool = config.APLICAR_NORMALIZACAO
    colunas_para_normalizar: Optional[List[str]] = config.COLUNAS_NORMALIZAR
    metodo_normalizacao: str = config.METODO_NORMALIZACAO
    normalizar_por_agrupamento: Optional[str] = config.AGRUPAMENTO_NORMALIZAR
    sufixo_colunas_normalizadas: str = config.SUFIXO_NORMALIZADAS
    salvar_mapeamentos: bool = config.SALVAR_MAPEAMENTOS
    diretorio_artefatos: str = config.DIRETORIO_ARTEFATOS


ProcCfg = ConfiguracaoProcessamento


def processar_df(df: pd.DataFrame,
                 cfg: Union[ProcCfg, Dict, None] = None
                 ) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """
    Retorna (df_processado, artefatos) onde artefatos inclui mapeamentos de codificacao.
    """
    if isinstance(cfg, dict):
        cfg = ProcCfg(**{k: v for k, v in cfg.items() if k in ProcCfg.__dataclass_fields__})
    cfg = cfg or ProcCfg()

    X = df.copy()
    # cabeçalho em minúsculas e sem espaços
    X.columns = [c.lower().strip().replace(" ", "_") for c in X.columns]

    # 1) limpeza
    X = aplicar_substituicoes(X, cfg.substituicoes_limpeza)

    # 2) conversoes tipo
    X = converter_colunas_temporais(X, cfg.coluna_data, cfg.coluna_hora)
    X = converter_colunas_float(X, cfg.colunas_ponto_flutuante)
    X = converter_colunas_int(X, cfg.colunas_numeros_inteiros)
    X = converter_colunas_categoricas(X, cfg.colunas_categoricas)

    # 3) imputacao
    X = imputar_numericos(X, cfg.metodo_imputacao_numerica)
    X = imputar_categoricos(X, cfg.metodo_imputacao_categorica, cfg.valor_constante_categorica)

    # 4) temporais
    if cfg.criar_features_temporais:
        if cfg.criar_coluna_mes_ano:
            X = garantir_agrupamento_temporal(
                X, cfg.coluna_data, cfg.coluna_hora, nome_coluna="mes-ano"
            )
        else:
            X = converter_colunas_temporais(X, cfg.coluna_data, cfg.coluna_hora)

    # 5) derivadas
    if cfg.criar_features_derivadas:
        X = adicionar_features_derivadas(
            X, cfg.tipos_features_derivadas, cfg.sufixo_colunas_codificadas
        )

    artefatos: Dict[str, Dict] = {}

    # 6) codificacao
    if cfg.aplicar_codificacao and cfg.colunas_categoricas:
        cols_existentes = [c for c in cfg.colunas_categoricas if c in X.columns]
        if cfg.metodo_codificacao == "label":
            X, mapeamentos = aplicar_codificacao_label(
                X, cols_existentes, sufixo=cfg.sufixo_colunas_codificadas
            )
            artefatos["mapeamentos_codificacao"] = mapeamentos
        elif cfg.metodo_codificacao == "onehot":
            X = aplicar_one_hot(X, cols_existentes)

    # 7) normalizacao
    if cfg.aplicar_normalizacao:
        cols_norm = cfg.colunas_para_normalizar
        X = normalizar(
            X,
            colunas=cols_norm,
            metodo=cfg.metodo_normalizacao,
            agrupamento=cfg.normalizar_por_agrupamento,
            sufixo=cfg.sufixo_colunas_normalizadas,
        )

    return X, artefatos


__all__ = ["processar_df", "ConfiguracaoProcessamento", "ProcCfg"]
