"""
Avalia modelo em dados de teste com métricas detalhadas.
"""
from typing import Any, Dict
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from pycaret.classification import ClassificationExperiment
from config.logger_config import logger


def avaliar_modelo(
    exp: ClassificationExperiment,
    modelo,
    dados_teste: pd.DataFrame,
    coluna_alvo: str,
    average: str = "weighted",
) -> Dict[str, Any]:
    """
    Avalia modelo com métricas detalhadas.

    Args:
        exp (ClassificationExperiment): Experimento configurado
        modelo: Modelo treinado
        dados_teste (pd.DataFrame): Dados de teste
        coluna_alvo (str): Nome da coluna alvo
        average (str): Tipo de média para métricas multiclasse

    Returns:
        Dict contendo:
            - metricas: Dict com métricas numéricas
            - relatorio: String com classification report
            - matriz_confusao: Array com matriz de confusão
            - predicoes: DataFrame com predições
    """
    logger.info("Avaliando modelo em dados de teste...")

    # Faz predições
    predicoes_df = exp.predict_model(modelo, data=dados_teste)
    
    # Extrai valores reais e preditos
    y_true = dados_teste[coluna_alvo]
    y_pred = predicoes_df['prediction_label']
    
    # Calcula métricas
    metricas = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
    }
    
    # ROC AUC (apenas para classificação binária ou multiclasse com probabilidades)
    try:
        if len(y_true.unique()) == 2:
            # Binário: usa coluna de probabilidade da classe positiva
            y_proba = predicoes_df['prediction_score']
            metricas["roc_auc"] = float(roc_auc_score(y_true, y_proba))
        else:
            # Multiclasse: usa probabilidades de todas as classes
            proba_cols = [col for col in predicoes_df.columns if col.startswith('prediction_score_')]
            if proba_cols:
                y_proba = predicoes_df[proba_cols].values
                metricas["roc_auc"] = float(roc_auc_score(
                    y_true, y_proba, multi_class='ovr', average=average
                ))
    except Exception as e:
        logger.warning(f"Não foi possível calcular ROC AUC: {e}")
        metricas["roc_auc"] = None

    # Relatório de classificação
    relatorio = classification_report(y_true, y_pred, zero_division=0)
    
    # Matriz de confusão
    matriz = confusion_matrix(y_true, y_pred)

    logger.info(f"Avaliação concluída. Acurácia: {metricas['accuracy']:.4f}")

    return {
        "metricas": metricas,
        "relatorio": relatorio,
        "matriz_confusao": matriz,
        "predicoes": predicoes_df,
    }
