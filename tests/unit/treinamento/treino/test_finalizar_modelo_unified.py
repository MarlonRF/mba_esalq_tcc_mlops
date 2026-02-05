"""
Testes unitários para finalizar_modelo_unified.py
"""
import pytest
from unittest.mock import MagicMock
from src.treinamento.treino.finalizar_modelo_unified import finalizar_modelo


@pytest.fixture
def mock_exp():
    """Mock de experimento PyCaret."""
    exp = MagicMock()
    modelo_finalizado = MagicMock()
    modelo_finalizado.is_fitted = True
    exp.finalize_model.return_value = modelo_finalizado
    return exp


@pytest.fixture
def mock_modelo():
    """Mock de modelo."""
    return MagicMock()


def test_finalizar_modelo_classificacao(mock_exp, mock_modelo):
    """Testa finalização de modelo de classificação."""
    modelo_final = finalizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo
    )
    
    assert modelo_final is not None
    mock_exp.finalize_model.assert_called_once_with(mock_modelo)


def test_finalizar_modelo_regressao(mock_exp, mock_modelo):
    """Testa finalização de modelo de regressão."""
    modelo_final = finalizar_modelo(
        exp=mock_exp,
        tipo_problema='regressao',
        modelo=mock_modelo
    )
    
    assert modelo_final is not None
    mock_exp.finalize_model.assert_called_once_with(mock_modelo)


def test_finalizar_modelo_retorna_modelo_fitted(mock_exp, mock_modelo):
    """Testa que modelo finalizado tem atributo is_fitted."""
    modelo_final = finalizar_modelo(
        exp=mock_exp,
        tipo_problema='classificacao',
        modelo=mock_modelo
    )
    
    assert hasattr(modelo_final, 'is_fitted')
    assert modelo_final.is_fitted == True
