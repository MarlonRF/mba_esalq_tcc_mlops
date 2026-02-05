"""
Pipelines de processamento, engenharia de features e treinamento.

Pipelines disponíveis:
- pipeline_processamento: Apenas processamento base (limpeza, conversão, imputação)
- pipeline_features: Apenas engenharia de features (codificação, normalização, derivadas)
- pipeline_completo: Processamento + Features em uma única chamada
- pipeline_treinamento: Pipeline completo de treinamento de modelos
"""

from .pipeline_processamento import executar_pipeline_processamento
from .pipeline_features import executar_pipeline_features
from .pipeline_completo import executar_pipeline_completo

# Pipeline unificado de treinamento (recomendado)
from .pipeline_treinamento_unified import (
    treinar_pipeline_completo,
    treinar_rapido,
)

__all__ = [
    'executar_pipeline_processamento',
    'executar_pipeline_features',
    'executar_pipeline_completo',
    'treinar_pipeline_completo',
    'treinar_rapido',
]
