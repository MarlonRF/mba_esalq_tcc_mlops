"""
Constantes e configurações para treinamento de modelos.
"""

# Mapeamento de nomes dos plots do PyCaret para descrições legíveis
PYCARET_PLOTS = {
    "pipeline": "Esquema do pipeline de pré-processamento",
    "auc": "Área sob a curva ROC",
    "threshold": "Threshold de discriminação",
    "pr": "Curva de precisão-recall",
    "confusion_matrix": "Matriz de confusão",
    "error": "Erro de predição de classe",
    "class_report": "Relatório de classificação",
    "boundary": "Fronteira de decisão",
    "rfe": "Seleção recursiva de atributos",
    "learning": "Curva de aprendizado",
    "manifold": "Aprendizado de variedades",
    "calibration": "Curva de calibração",
    "vc": "Curva de validação",
    "dimension": "Aprendizado de dimensão",
    "feature": "Importância das features",
    "feature_all": "Importância das features (todas)",
    "parameter": "Hiperparâmetros do modelo",
    "lift": "Curva de lift",
    "gain": "Gráfico de ganho",
    "tree": "Árvore de decisão",
    "ks": "Gráfico KS Statistic",
}

# Métricas de avaliação padrão para classificação
METRICAS_CLASSIFICACAO = ["Accuracy", "AUC", "Recall", "Prec.", "F1", "Kappa", "MCC"]

# Métricas de avaliação padrão para regressão
METRICAS_REGRESSAO = ["MAE", "MSE", "RMSE", "R2", "RMSLE", "MAPE"]

# Configuração padrão para treinamento
PARAMS_PADRAO = {
    "remove_outliers": True,
    "pca": False,
    "outliers_method": "iforest",
    "session_id": None,
    "normalize": True,
    "fold": 5,
    "verbose": False,
    "html": False,
    "use_gpu": True,
    "log_experiment": False,
}
