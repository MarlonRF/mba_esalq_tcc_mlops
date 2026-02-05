"""
Testes unitários para configurar_parametros.py
"""
import pytest
from src.treinamento.configuracao.configurar_parametros import configurar_parametros


def test_configurar_parametros_sem_customizacao():
    """Testa que retorna parâmetros padrão quando não há customização."""
    resultado = configurar_parametros()
    
    assert isinstance(resultado, dict)
    assert 'session_id' in resultado
    assert 'verbose' in resultado


def test_configurar_parametros_merge_customizados():
    """Testa merge de parâmetros customizados com padrões."""
    params_custom = {
        'fold': 3,
        'normalize': False
    }
    
    resultado = configurar_parametros(params_custom)
    
    assert resultado['fold'] == 3
    assert resultado['normalize'] == False
    # Deve manter outros parâmetros padrão
    assert 'session_id' in resultado


def test_configurar_parametros_sobrescreve_padrao():
    """Testa que parâmetros customizados sobrescrevem padrões."""
    params_custom = {
        'session_id': 999
    }
    
    resultado = configurar_parametros(params_custom)
    
    assert resultado['session_id'] == 999


def test_configurar_parametros_nao_modifica_original():
    """Testa que dicionário original não é modificado."""
    params_custom = {'fold': 5}
    original_keys = set(params_custom.keys())
    
    configurar_parametros(params_custom)
    
    # Original deve permanecer inalterado
    assert set(params_custom.keys()) == original_keys
