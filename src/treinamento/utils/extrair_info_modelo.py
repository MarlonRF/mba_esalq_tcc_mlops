"""
Extrai informações básicas de um modelo.
"""
from typing import Any, Dict
from .extrair_estimador import extrair_estimador


def extrair_info_modelo(modelo: Any) -> Dict[str, Any]:
    """
    Extrai informações básicas de um modelo (nome, parâmetros, classes, features).

    Args:
        modelo: Modelo ou pipeline do qual extrair informações

    Returns:
        Dict contendo:
            - modelo_nome: Nome do modelo
            - parametros: Dicionário com hiperparâmetros
            - classes: Classes do modelo (se disponível)
            - n_features: Número de features (se disponível)
    """
    estimador = extrair_estimador(modelo)
    nome = estimador.__class__.__name__
    
    # Extrai parâmetros
    try:
        parametros = estimador.get_params(deep=False)
    except Exception:
        parametros = {}
    
    # Extrai classes (para classificação)
    classes = None
    try:
        classes = list(estimador.classes_)
    except AttributeError:
        pass
    
    # Extrai número de features
    n_features = None
    try:
        n_features = estimador.n_features_in_
    except AttributeError:
        pass
    
    return {
        "modelo_nome": nome,
        "parametros": parametros,
        "classes": classes,
        "n_features": n_features,
    }
