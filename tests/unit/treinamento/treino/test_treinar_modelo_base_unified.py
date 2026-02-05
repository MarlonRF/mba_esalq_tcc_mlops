"""
Testes unitários para treinar_modelo_base_unified.py
"""
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.treinamento.treino.treinar_modelo_base_unified import treinar_modelo_base


@pytest.fixture
def mock_exp_classificacao():
    """Mock de ClassificationExperiment."""
    exp = MagicMock()
    exp.compare_models.return_value = [MagicMock(), MagicMock()]
    exp.pull.return_value = pd.DataFrame({
        'Model': ['lr', 'dt'],
        'Accuracy': [0.85, 0.80],
        'AUC': [0.90, 0.85]
    })
    return exp


@pytest.fixture
def mock_exp_regressao():
    """Mock de RegressionExperiment."""
    exp = MagicMock()
    exp.compare_models.return_value = [MagicMock(), MagicMock()]
    exp.pull.return_value = pd.DataFrame({
        'Model': ['lr', 'ridge'],
        'MAE': [5.2, 6.1],
        'R2': [0.85, 0.80]
    })
    return exp


def test_treinar_modelo_base_classificacao(mock_exp_classificacao):
    """Testa treinamento de modelos base para classificação."""
    modelos, tabela = treinar_modelo_base(
        exp=mock_exp_classificacao,
        tipo_problema='classificacao',
        n_select=2
    )
    
    assert len(modelos) == 2
    assert isinstance(tabela, pd.DataFrame)
    mock_exp_classificacao.compare_models.assert_called_once()


def test_treinar_modelo_base_regressao(mock_exp_regressao):
    """Testa treinamento de modelos base para regressão."""
    modelos, tabela = treinar_modelo_base(
        exp=mock_exp_regressao,
        tipo_problema='regressao',
        n_select=2
    )
    
    assert len(modelos) == 2
    assert isinstance(tabela, pd.DataFrame)
    mock_exp_regressao.compare_models.assert_called_once()


def test_treinar_modelo_base_n_select_1(mock_exp_classificacao):
    """Testa que n_select=1 retorna lista com 1 modelo."""
    mock_exp_classificacao.compare_models.return_value = MagicMock()  # Retorna modelo único
    
    modelos, tabela = treinar_modelo_base(
        exp=mock_exp_classificacao,
        tipo_problema='classificacao',
        n_select=1
    )
    
    assert isinstance(modelos, list)
    assert len(modelos) == 1


def test_treinar_modelo_base_com_include(mock_exp_classificacao):
    """Testa filtragem com lista de include."""
    treinar_modelo_base(
        exp=mock_exp_classificacao,
        tipo_problema='classificacao',
        n_select=2,
        include=['lr', 'dt']
    )
    
    mock_exp_classificacao.compare_models.assert_called_once()
    call_kwargs = mock_exp_classificacao.compare_models.call_args[1]
    assert call_kwargs['include'] == ['lr', 'dt']


def test_treinar_modelo_base_com_exclude(mock_exp_classificacao):
    """Testa filtragem com lista de exclude."""
    treinar_modelo_base(
        exp=mock_exp_classificacao,
        tipo_problema='classificacao',
        n_select=2,
        exclude=['svm']
    )
    
    call_kwargs = mock_exp_classificacao.compare_models.call_args[1]
    assert call_kwargs['exclude'] == ['svm']


def test_treinar_modelo_base_com_sort(mock_exp_classificacao):
    """Testa ordenação por métrica específica."""
    treinar_modelo_base(
        exp=mock_exp_classificacao,
        tipo_problema='classificacao',
        n_select=2,
        sort='AUC'
    )
    
    call_kwargs = mock_exp_classificacao.compare_models.call_args[1]
    assert call_kwargs['sort'] == 'AUC'
