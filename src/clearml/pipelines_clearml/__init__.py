"""
__init__.py para pipelines_clearml.

Importa pipelines integrados com ClearML.
"""

from .pipeline_processamento_clearml import executar_pipeline_processamento_clearml
from .pipeline_features_clearml import executar_pipeline_features_clearml
from .pipeline_treinamento_clearml import executar_pipeline_treinamento_clearml

__all__ = [
    'executar_pipeline_processamento_clearml',
    'executar_pipeline_features_clearml',
    'executar_pipeline_treinamento_clearml',
]
