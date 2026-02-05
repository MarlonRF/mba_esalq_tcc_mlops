"""
Testes unitários para extrair_estimador.py
"""
import pytest
from unittest.mock import MagicMock
from src.treinamento.utils.extrair_estimador import extrair_estimador


def test_extrair_estimador_com_pipeline():
    """Testa extração de estimador de pipeline PyCaret."""
    # Mock de pipeline com named_steps
    mock_estimador = MagicMock()
    mock_pipeline = MagicMock()
    mock_pipeline.named_steps = {'trained_model': mock_estimador}
    
    resultado = extrair_estimador(mock_pipeline)
    
    assert resultado == mock_estimador


def test_extrair_estimador_sem_trained_model():
    """Testa extração quando 'trained_model' não existe, pega último step."""
    mock_step1 = MagicMock()
    mock_step2 = MagicMock()
    mock_pipeline = MagicMock()
    mock_pipeline.named_steps = {'preprocessor': mock_step1, 'estimator': mock_step2}
    
    resultado = extrair_estimador(mock_pipeline)
    
    assert resultado == mock_step2


def test_extrair_estimador_sem_pipeline():
    """Testa que retorna o próprio modelo se não for pipeline."""
    mock_modelo = MagicMock()
    del mock_modelo.named_steps  # Garante que não tem named_steps
    
    resultado = extrair_estimador(mock_modelo)
    
    assert resultado == mock_modelo


def test_extrair_estimador_modelo_direto():
    """Testa extração de modelo que já é o estimador."""
    mock_estimador = MagicMock()
    mock_estimador.named_steps = None
    
    resultado = extrair_estimador(mock_estimador)
    
    assert resultado == mock_estimador
