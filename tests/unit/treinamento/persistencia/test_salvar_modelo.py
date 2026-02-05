"""
Testes unitários para salvar_modelo.py
"""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.treinamento.persistencia.salvar_modelo import salvar_modelo


def test_salvar_modelo_cria_pasta():
    """Testa que pasta de destino é criada se não existir."""
    mock_exp = MagicMock()
    mock_modelo = MagicMock()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        pasta_destino = os.path.join(tmpdir, 'nova_pasta')
        
        with patch.object(mock_exp, 'save_model'):
            caminho = salvar_modelo(
                exp=mock_exp,
                modelo=mock_modelo,
                nome_modelo='teste',
                pasta_destino=pasta_destino
            )
        
        assert os.path.exists(pasta_destino)
        assert caminho.endswith('.pkl')


def test_salvar_modelo_retorna_caminho_completo():
    """Testa que retorna caminho completo com extensão .pkl."""
    mock_exp = MagicMock()
    mock_modelo = MagicMock()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(mock_exp, 'save_model'):
            caminho = salvar_modelo(
                exp=mock_exp,
                modelo=mock_modelo,
                nome_modelo='meu_modelo',
                pasta_destino=tmpdir
            )
        
        assert caminho == os.path.join(tmpdir, 'meu_modelo.pkl')


def test_salvar_modelo_chama_save_model():
    """Testa que exp.save_model é chamado com argumentos corretos."""
    mock_exp = MagicMock()
    mock_modelo = MagicMock()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(mock_exp, 'save_model') as mock_save:
            salvar_modelo(
                exp=mock_exp,
                modelo=mock_modelo,
                nome_modelo='teste',
                pasta_destino=tmpdir
            )
            
            # Verifica chamada com caminho base (sem .pkl)
            esperado = os.path.join(tmpdir, 'teste')
            mock_save.assert_called_once_with(mock_modelo, esperado)


def test_salvar_modelo_pasta_padrao():
    """Testa uso de pasta padrão 'modelos'."""
    mock_exp = MagicMock()
    mock_modelo = MagicMock()
    
    with patch('os.makedirs'):
        with patch.object(mock_exp, 'save_model'):
            caminho = salvar_modelo(
                exp=mock_exp,
                modelo=mock_modelo,
                nome_modelo='teste'
            )
    
    assert 'modelos' in caminho
    assert caminho.endswith('.pkl')
