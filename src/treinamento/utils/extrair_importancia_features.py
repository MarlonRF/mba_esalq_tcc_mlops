"""
Extrai importância de features usando RandomForest.
"""
from typing import Dict, List
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def extrair_importancia_features(
    dados: pd.DataFrame,
    coluna_alvo: str,
    atributos: List[str] | None = None,
    n_top_features: int | None = None,
    random_state: int = 42,
) -> Dict[str, pd.DataFrame]:
    """
    Treina um RandomForest e extrai importância das features.

    Args:
        dados (pd.DataFrame): DataFrame com dados de treino
        coluna_alvo (str): Nome da coluna alvo
        atributos (List[str], optional): Lista de atributos a usar. Se None, usa todos exceto alvo
        n_top_features (int, optional): Número de top features a retornar. Se None, retorna todas
        random_state (int): Seed para reprodutibilidade

    Returns:
        Dict contendo:
            - 'importancias': DataFrame com feature e importância ordenado
            - 'top_features': Lista com nomes das top N features (se n_top_features especificado)
            - 'modelo': Modelo RandomForest treinado
    """
    if atributos is None:
        X = dados.drop(columns=[coluna_alvo])
    else:
        X = dados[atributos]
    y = dados[coluna_alvo]

    # Treina RandomForest
    clf = RandomForestClassifier(random_state=random_state, n_estimators=100)
    clf.fit(X, y)

    # Extrai importâncias
    importancias = pd.DataFrame({
        'feature': X.columns,
        'importancia': clf.feature_importances_
    }).sort_values('importancia', ascending=False).reset_index(drop=True)

    resultado = {
        'importancias': importancias,
        'modelo': clf
    }

    # Se especificado, retorna top N features
    if n_top_features is not None:
        resultado['top_features'] = importancias['feature'].head(n_top_features).tolist()

    return resultado
