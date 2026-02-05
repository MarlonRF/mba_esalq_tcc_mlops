"""
Imputacao de valores faltantes categoricos.
"""
import pandas as pd


def imputar_categoricos(
    df: pd.DataFrame,
    metodo: str = "mode",
    valor_constante: str = "__missing__",
) -> pd.DataFrame:
    """Imputa colunas categoricas com mode ou constante."""
    if metodo not in {"mode", "const"}:
        return df
    df = df.copy()
    cat_cols = [c for c in df.select_dtypes(include=["string", "object"]).columns]
    for c in cat_cols:
        if metodo == "mode":
            if df[c].notna().any():
                df[c] = df[c].fillna(df[c].mode(dropna=True).iloc[0])
            else:
                df[c] = df[c].fillna(valor_constante)
        else:
            df[c] = df[c].fillna(valor_constante)
    return df
