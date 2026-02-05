"""
Testes unitários para otimizar_modelo_unified.py
"""
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.treinamento.treino.otimizar_modelo_unified import otimizar_modelo


@pytest.fixture
def mock_exp():
    """Mock de experimento PyCaret."""
    exp = MagicMock()
    exp.tune_model.return_value = MagicMock()
    exp.pull.return_value = pd.DataFrame({
        'Accuracy': [0.90],
        'AUC': [0.92]
    })
    return exp


@pytest.fixture
def mock_modelo():
    """Mock de modelo."""
    modelo = MagicMock()
    modelo.__class__.__name__ = 'LogisticRegression'
    return modelo


@patch('src.treinamento.treino.otimizar_modelo_unified.extrair_info_modelo')
def test_otimizar_modelo_classificacao(mock_extrair, mock_exp, mock_modelo):
    """Testa otimização de modelo de classificação."""
    mock_extrair.return_value = {'modelo_nome': 'LogisticRegression'}
    
    modelo_otimizado, metricas = otimizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo,
        n_iter=5
    )
    
    assert modelo_otimizado is not None
    assert isinstance(metricas, pd.DataFrame)
    mock_exp.tune_model.assert_called_once()


@patch('src.treinamento.treino.otimizar_modelo_unified.extrair_info_modelo')
def test_otimizar_modelo_regressao(mock_extrair, mock_exp, mock_modelo):
    """Testa otimização de modelo de regressão."""
    mock_extrair.return_value = {'modelo_nome': 'LinearRegression'}
    mock_exp.pull.return_value = pd.DataFrame({'MAE': [3.5], 'R2': [0.85]})
    
    modelo_otimizado, metricas = otimizar_modelo(
        exp=mock_exp,
        tipo_problema='regressao',
        modelo=mock_modelo,
        n_iter=5
    )
    
    assert modelo_otimizado is not None
    # Verifica que métrica padrão para regressão é R2
    call_kwargs = mock_exp.tune_model.call_args[1]
    assert call_kwargs['optimize'] == 'R2'


@patch('src.treinamento.treino.otimizar_modelo_unified.extrair_info_modelo')
def test_otimizar_modelo_metrica_customizada(mock_extrair, mock_exp, mock_modelo):
    """Testa otimização com métrica customizada."""
    mock_extrair.return_value = {'modelo_nome': 'RandomForest'}
    
    otimizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo,
        optimize='F1',
        n_iter=10
    )
    
    call_kwargs = mock_exp.tune_model.call_args[1]
    assert call_kwargs['optimize'] == 'F1'
    assert call_kwargs['n_iter'] == 10


@patch('src.treinamento.treino.otimizar_modelo_unified.extrair_info_modelo')
def test_otimizar_modelo_custom_grid(mock_extrair, mock_exp, mock_modelo):
    """Testa otimização com grade personalizada."""
    mock_extrair.return_value = {'modelo_nome': 'RandomForest'}
    custom_grid = {'n_estimators': [100, 200], 'max_depth': [5, 10]}
    
    otimizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo,
        custom_grid=custom_grid
    )
    
    call_kwargs = mock_exp.tune_model.call_args[1]
    assert call_kwargs['custom_grid'] == custom_grid


@patch('src.treinamento.treino.otimizar_modelo_unified.extrair_info_modelo')
def test_otimizar_modelo_metrica_padrao_classificacao(mock_extrair, mock_exp, mock_modelo):
    """Testa que métrica padrão para classificação é Accuracy."""
    mock_extrair.return_value = {'modelo_nome': 'LogisticRegression'}
    
    otimizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo
    )
    
    call_kwargs = mock_exp.tune_model.call_args[1]
    assert call_kwargs['optimize'] == 'Accuracy'
