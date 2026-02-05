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
    nome = (nome or "standard").lower()
    cls = SCALERS.get(nome, StandardScaler)
    return cls()

