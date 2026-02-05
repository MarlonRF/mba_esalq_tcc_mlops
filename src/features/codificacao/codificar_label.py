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
    # Criar códigos únicos
    valores_unicos = serie.dropna().unique()
    mapeamento = {val: idx for idx, val in enumerate(valores_unicos)}
    mapeamento_inverso = {idx: val for val, idx in mapeamento.items()}
    
    # Aplicar mapeamento
    serie_codificada = serie.map(mapeamento)
    
    return serie_codificada, mapeamento_inverso
