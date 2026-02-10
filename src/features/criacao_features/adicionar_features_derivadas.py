"""
Adicao de features derivadas.
"""
from typing import List
import pandas as pd
from .calcular_valor_imc import calcular_valor_imc
from .imc_classe import imc_classe
from .calcular_heat_index import calcular_heat_index
from .calcular_ponto_orvalho import calcular_ponto_orvalho


def adicionar_features_derivadas(
    df: pd.DataFrame,
    tipos: List[str],
    sufixo_codificado: str = "_cod",
) -> pd.DataFrame:
    """Adiciona features derivadas selecionadas pela lista tipos."""
    if not tipos:
        return df
    df = df.copy()
    coluna_temp = "tmedia" if "tmedia" in df.columns else "temperatura"
    coluna_umidade = "ur" if "ur" in df.columns else "umidade"

    # IMC e classe
    if "imc" in tipos and {"peso", "altura"}.issubset(df.columns):
        df["imc"] = df.apply(lambda r: calcular_valor_imc(r.get("peso"), r.get("altura")), axis=1)
    if "imc_classe" in tipos and "imc" in df.columns:
        df["imc_classe"] = df["imc"].apply(imc_classe)

    # Heat index
    if "heat_index" in tipos and {coluna_temp, coluna_umidade}.issubset(df.columns):
        df["heat_index"] = df.apply(
            lambda r: calcular_heat_index(r.get(coluna_temp), r.get(coluna_umidade)),
            axis=1,
        )

    # Dew point
    if "dew_point" in tipos and {coluna_temp, coluna_umidade}.issubset(df.columns):
        df["dew_point"] = df.apply(
            lambda r: calcular_ponto_orvalho(r.get(coluna_temp), r.get(coluna_umidade)),
            axis=1,
        )

    # Interacoes simples
    if "t*u" in tipos and {coluna_temp, coluna_umidade}.issubset(df.columns):
        valor_tu = df[coluna_temp] * df[coluna_umidade]
        df["t*u"] = valor_tu
        df["t_u"] = valor_tu
    if "t/u" in tipos and {coluna_temp, coluna_umidade}.issubset(df.columns):
        df["t/u"] = df[coluna_temp] / df[coluna_umidade]

    # Ajusta nomes codificados se necessário
    if sufixo_codificado and "sexo" in df.columns:
        col_cod = f"sexo{sufixo_codificado}"
        if col_cod in df.columns:
            df[col_cod] = df[col_cod].astype("Int64")

    return df
