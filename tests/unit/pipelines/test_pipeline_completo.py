"""
Testes unitários para pipeline_completo.py
"""
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd


@pytest.fixture
def df_exemplo():
    """DataFrame de exemplo para testes."""
    return pd.DataFrame({
        'col1': [1, 2, 3, None, 5],
        'col2': ['A', 'B', 'A', 'B', 'A'],
        'target': [0, 1, 0, 1, 0]
    })


@patch('src.pipelines.pipeline_completo.executar_pipeline_processamento')
@patch('src.pipelines.pipeline_completo.executar_pipeline_features')
@patch('src.pipelines.pipeline_completo.treinar_pipeline_completo')
def test_pipeline_completo_mock(mock_treino, mock_features, mock_proc, df_exemplo):
    """Testa pipeline completo com mocks."""
    from src.pipelines.pipeline_completo import executar_pipeline_completo_ml
    
    # Configura retornos dos mocks
    mock_proc.return_value = df_exemplo
    mock_features.return_value = (df_exemplo, {'scaler': MagicMock()})
    mock_treino.return_value = {
        'melhor_modelo': MagicMock(),
        'metricas_melhor': {'Accuracy': 0.85}
    }
    
    # Executa pipeline
    resultado = executar_pipeline_completo_ml(
        dados=df_exemplo,
        coluna_alvo='target',
        tipo_problema='classificacao'
    )
    
    # Verifica que todas as etapas foram chamadas
    mock_proc.assert_called_once()
    mock_features.assert_called_once()
    mock_treino.assert_called_once()
    
    # Verifica resultado
    assert 'melhor_modelo' in resultado
