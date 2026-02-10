"""
Módulo de utilitários para integração com ClearML.

Este módulo contém funções auxiliares modulares para:
- Verificação de disponibilidade do ClearML
- Gerenciamento de tasks
- Gerenciamento de datasets
- Integração de artefatos (dataframes, métricas, gráficos)
- Carregamento de credenciais
"""

from .verificador_clearml import obter_clearml_disponivel, garantir_clearml_disponivel
from .operacoes_task import criar_task, obter_task_atual
from .operacoes_dataset import criar_dataset, buscar_dataset
from .integracao_artefatos import (
    registrar_dataframe,
    registrar_metricas,
    registrar_arquivo
)
from .credenciais_clearml import carregar_credenciais_clearml, configurar_clearml_online

__all__ = [
    # Verificação ClearML
    'obter_clearml_disponivel',
    'garantir_clearml_disponivel',
    # Operações de Task
    'criar_task',
    'obter_task_atual',
    # Operações de Dataset
    'criar_dataset',
    'buscar_dataset',
    # Integração de Artefatos
    'registrar_dataframe',
    'registrar_metricas',
    'registrar_arquivo',
    # Credenciais
    'carregar_credenciais_clearml',
    'configurar_clearml_online',
]
