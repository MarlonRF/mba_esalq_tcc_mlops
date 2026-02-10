"""
Codificacao label: converte valores categoricos em codigos numericos.
"""
from typing import Dict, Tuple
import pandas as pd


def codificar_label(serie: pd.Series) -> Tuple[pd.Series, Dict[int, str]]:
    """
    Codifica uma Serie categórica em códigos numéricos.
    
    Args:
        serie: Serie com valores categóricos
        
    Returns:
        Tupla (serie_codificada, mapeamento_inverso)
        onde mapeamento_inverso é {codigo: valor_original}
    """
    serie_limpa = serie.astype("string").fillna("__faltante__")

    # Mantém a ordem de aparição das categorias para mapeamento estável.
    valores_unicos = serie_limpa.unique().tolist()
    mapeamento = {valor: indice for indice, valor in enumerate(valores_unicos)}
    mapeamento_inverso = {indice: str(valor) for valor, indice in mapeamento.items()}

    serie_codificada = serie_limpa.map(mapeamento).astype("Int64")

    return serie_codificada, mapeamento_inverso
