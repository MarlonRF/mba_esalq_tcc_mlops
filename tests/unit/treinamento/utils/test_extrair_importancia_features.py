"""
Testes unitários para extrair_importancia_features.py
"""
import pytest
import pandas as pd
import numpy as np
from src.treinamento.utils.extrair_importancia_features import extrair_importancia_features


@pytest.fixture
def dados_classificacao():
    """Dataset sintético para classificação."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'feature3': np.random.rand(100),
        'target': np.random.randint(0, 2, 100)
    })


def test_extrair_importancia_features_basico(dados_classificacao):
    """Testa extração básica de importância de features."""
    resultado = extrair_importancia_features(
        dados=dados_classificacao,
        coluna_alvo='target'
    )
    
    assert 'importancias' in resultado
    assert 'modelo' in resultado
    assert isinstance(resultado['importancias'], pd.DataFrame)
    assert 'feature' in resultado['importancias'].columns
    assert 'importancia' in resultado['importancias'].columns
    assert len(resultado['importancias']) == 3  # 3 features


def test_extrair_importancia_features_com_atributos_especificos(dados_classificacao):
    """Testa com lista específica de atributos."""
    resultado = extrair_importancia_features(
        dados=dados_classificacao,
        coluna_alvo='target',
        atributos=['feature1', 'feature2']
    )
    
    assert len(resultado['importancias']) == 2


def test_extrair_importancia_features_top_n(dados_classificacao):
    """Testa retorno de top N features."""
    resultado = extrair_importancia_features(
        dados=dados_classificacao,
        coluna_alvo='target',
        n_top_features=2
    )
    
    assert 'top_features' in resultado
    assert len(resultado['top_features']) == 2


def test_extrair_importancia_features_ordenado(dados_classificacao):
    """Testa que importâncias estão ordenadas decrescente."""
    resultado = extrair_importancia_features(
        dados=dados_classificacao,
        coluna_alvo='target'
    )
    
    importancias = resultado['importancias']['importancia'].values
    assert all(importancias[i] >= importancias[i+1] for i in range(len(importancias)-1))


def test_extrair_importancia_features_soma_um(dados_classificacao):
    """Testa que importâncias somam aproximadamente 1."""
    resultado = extrair_importancia_features(
        dados=dados_classificacao,
        coluna_alvo='target'
    )
    
    soma = resultado['importancias']['importancia'].sum()
    assert abs(soma - 1.0) < 0.01  # Tolerância para erros de ponto flutuante
