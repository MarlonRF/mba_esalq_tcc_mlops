"""
Testes unitários para carregar_modelo.py
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.treinamento.persistencia.carregar_modelo import carregar_modelo


def test_carregar_modelo_sucesso():
    """Testa carregamento bem-sucedido de modelo."""
    mock_modelo = MagicMock()
    
    with patch('src.treinamento.persistencia.carregar_modelo.load_model', return_value=mock_modelo):
        resultado = carregar_modelo('modelos/meu_modelo')
        
        assert resultado == mock_modelo


def test_carregar_modelo_remove_extensao_pkl():
    """Testa que extensão .pkl é removida automaticamente."""
    mock_modelo = MagicMock()
    
    with patch('src.treinamento.persistencia.carregar_modelo.load_model', return_value=mock_modelo) as mock_load:
        carregar_modelo('modelos/meu_modelo.pkl')
        
        # Verifica que load_model foi chamado sem .pkl
        mock_load.assert_called_once_with('modelos/meu_modelo')


def test_carregar_modelo_caminho_sem_extensao():
    """Testa carregamento com caminho sem extensão."""
    mock_modelo = MagicMock()
    
    with patch('src.treinamento.persistencia.carregar_modelo.load_model', return_value=mock_modelo) as mock_load:
        carregar_modelo('modelos/meu_modelo')
        
        mock_load.assert_called_once_with('modelos/meu_modelo')


def test_carregar_modelo_arquivo_inexistente():
    """Testa erro quando arquivo não existe."""
    with patch('src.treinamento.persistencia.carregar_modelo.load_model', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            carregar_modelo('modelos/nao_existe')
