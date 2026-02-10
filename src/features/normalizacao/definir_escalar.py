"""
Selecao de scaler.
"""
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, Normalizer, RobustScaler, StandardScaler


SCALERS = {
    "standard": StandardScaler,
    "minmax": MinMaxScaler,
    "robust": RobustScaler,
    "max": MaxAbsScaler,
    "l2": Normalizer,
}


def pick_scaler(nome: str):
    """
    Retorna um scaler instanciado baseado no nome.
    
    Args:
        nome: Nome do scaler ('standard', 'minmax', 'robust', 'max', 'l2')
        
    Returns:
        Instância do scaler sklearn
    """
    nome_normalizado = (nome or "standard").lower()
    cls = SCALERS.get(nome_normalizado)
    if cls is None:
        disponiveis = ", ".join(sorted(SCALERS.keys()))
        raise ValueError(f"Metodo de normalizacao invalido: {nome}. Opcoes: {disponiveis}")
    return cls()

