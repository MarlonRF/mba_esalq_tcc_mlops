"""
Funcoes auxiliares do pipeline de processamento de conforto termico.
Separadas para facilitar manutencao e testes unitarios.
"""
from typing import Dict, Tuple

import os

import numpy as np
import pandas as pd

def _converter_para_float(serie_dados: pd.Series) -> pd.Series:
    """Converte serie para float tratando virgula decimal."""
    serie_tratada = serie_dados.astype(str).str.replace(",", ".", regex=False)
    return pd.to_numeric(serie_tratada, errors="coerce")


def _garantir_diretorio_existe(caminho_arquivo: str) -> None:
    diretorio = os.path.dirname(caminho_arquivo) or "."
    os.makedirs(diretorio, exist_ok=True)


def _codificar_com_labels(serie_dados: pd.Series) -> Tuple[pd.Series, Dict[int, str]]:
    serie_string = serie_dados.astype("string").fillna("__faltante__")
    categorias = pd.Categorical(serie_string)
    codigos_numericos = pd.Series(categorias.codes).astype("Int64")
    mapeamento_codigos = {
        int(codigo): str(categoria)
        for codigo, categoria in enumerate(categorias.categories)
    }
    return codigos_numericos, mapeamento_codigos


def _calcular_indice_calor(
    temperatura_celsius: float, umidade_relativa: float
) -> float:
    if pd.isna(temperatura_celsius) or pd.isna(umidade_relativa):
        return np.nan
    indice_calor = (
        -8.78469475556
        + 1.61139411 * temperatura_celsius
        + 2.33854883889 * umidade_relativa
        - 0.14611605 * temperatura_celsius * umidade_relativa
    )
    return indice_calor


def _calcular_ponto_orvalho(
    temperatura_celsius: float, umidade_relativa: float
) -> float:
    if pd.isna(temperatura_celsius) or pd.isna(umidade_relativa):
        return np.nan
    return temperatura_celsius - ((100.0 - umidade_relativa) / 5.0)


def _calcular_imc(peso_kg: float, altura_cm: float) -> float:
    if pd.isna(peso_kg) or pd.isna(altura_cm) or altura_cm == 0:
        return np.nan
    altura_metros = altura_cm / 100.0
    return peso_kg / (altura_metros**2)


def _imc_classe(v: float) -> str:
    if pd.isna(v):
        return np.nan
    if v < 18.5:
        return "Abaixo do peso"
    if v < 25:
        return "Peso Normal"
    if v < 30:
        return "Sobrepeso"
    if v < 35:
        return "Obesidade Grau I"
    if v < 40:
        return "Obesidade Grau II"
    return "Obesidade Grau III"


def _pick_scaler(name: str):
    from sklearn.preprocessing import (
        MaxAbsScaler,
        MinMaxScaler,
        Normalizer,
        RobustScaler,
        StandardScaler,
    )

    name = (name or "standard").lower()
    if name == "minmax":
        return MinMaxScaler()
    if name == "robust":
        return RobustScaler()
    if name == "max":
        return MaxAbsScaler()
    if name == "l2":
        return Normalizer()
    return StandardScaler()


__all__ = [
    "_converter_para_float",
    "_garantir_diretorio_existe",
    "_codificar_com_labels",
    "_calcular_indice_calor",
    "_calcular_ponto_orvalho",
    "_calcular_imc",
    "_imc_classe",
    "_pick_scaler",
]
