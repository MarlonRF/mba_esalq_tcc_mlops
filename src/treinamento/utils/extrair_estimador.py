"""
Extrai o estimador principal de um pipeline do PyCaret.
"""
from typing import Any


def extrair_estimador(modelo_pipeline: Any) -> Any:
    """
    Extrai o estimador principal de um pipeline do PyCaret.

    Modelos do PyCaret são wrappers/pipelines que contêm o estimador sklearn real.
    Esta função extrai o estimador base para acesso direto aos métodos sklearn.

    Args:
        modelo_pipeline: Pipeline ou modelo do PyCaret

    Returns:
        O estimador/modelo sklearn subjacente
        
    Examples:
        >>> from pycaret.classification import create_model
        >>> modelo_pycaret = create_model('lr')
        >>> estimador_sklearn = extrair_estimador(modelo_pycaret)
        >>> # Agora pode usar métodos sklearn diretamente
        >>> estimador_sklearn.predict_proba(X_test)
    """
    # Em PyCaret o estimador costuma estar em 'trained_model';
    # se não, pega o último passo do pipeline.
    steps = getattr(modelo_pipeline, "named_steps", None)
    if steps:
        est = steps.get("trained_model", list(steps.values())[-1])
    elif hasattr(modelo_pipeline, "estimator") and not callable(getattr(modelo_pipeline, "fit", None)):
        est = getattr(modelo_pipeline, "estimator")
    else:
        est = modelo_pipeline
    return est
