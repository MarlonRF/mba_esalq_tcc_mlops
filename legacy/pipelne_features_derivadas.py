"""
Adicao de features derivadas.
"""
from typing import List
import pandas as pd
from ..processamento.derivadas.calcular_valor_imc import calcular_imc
from ..processamento.derivadas.imc_classe import imc_classe
from ..processamento.derivadas.calcular_heat_index import calcular_heat_index
from ..processamento.derivadas.calcular_ponto_orvalho import calcular_ponto_orvalho


def adicionar_features_derivadas(
    df: pd.DataFrame,
    tipos: List[str],
    sufixo_codificado: str = "_cod",
) -> pd.DataFrame:
    """Adiciona features derivadas selecionadas pela lista tipos."""
    if not tipos:
        return df
    df = df.copy()

    # IMC e classe
    if "imc" in tipos and {"peso", "altura"}.issubset(df.columns):
        df["IMC"] = df.apply(lambda r: calcular_imc(r.get("peso"), r.get("altura")), axis=1)
    if "imc_classe" in tipos and "IMC" in df.columns:
        df["IMC_classe"] = df["IMC"].apply(imc_classe)

    # Heat index
    if "heat_index" in tipos and {"tmedia", "ur"}.issubset(df.columns):
        df["heat_index"] = df.apply(
            lambda r: calcular_heat_index(r.get("tmedia"), r.get("ur")), axis=1
        )

    # Dew point
    if "dew_point" in tipos and {"tmedia", "ur"}.issubset(df.columns):
        df["dew_point"] = df.apply(
            lambda r: calcular_ponto_orvalho(r.get("tmedia"), r.get("ur")), axis=1
        )

    # Interacoes simples
    if "t*u" in tipos and {"tmedia", "ur"}.issubset(df.columns):
        df["t_u"] = df["tmedia"] * df["ur"]
    if "t/u" in tipos and {"tmedia", "ur"}.issubset(df.columns):
        df["t_div_u"] = df["tmedia"] / df["ur"]

    # Ajusta nomes codificados se necessário
    if sufixo_codificado and "sexo" in df.columns:
        col_cod = f"sexo{sufixo_codificado}"
        if col_cod in df.columns:
            df[col_cod] = df[col_cod].astype("Int64")

    return df
