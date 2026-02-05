"""
Testes unitários para criar_experimento.py
"""
import pytest
import pandas as pd
from pycaret.classification import ClassificationExperiment
from pycaret.regression import RegressionExperiment
from src.treinamento.configuracao.criar_experimento import criar_experimento


@pytest.fixture
def dados_classificacao():
    """Dataset sintético para classificação."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    })


@pytest.fixture
def dados_regressao():
    """Dataset sintético para regressão."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'target': [10.5, 20.3, 30.1, 40.7, 50.2, 60.8, 70.4, 80.9, 90.6, 100.1]
    })


def test_criar_experimento_classificacao(dados_classificacao):
    """Testa criação de experimento de classificação."""
    exp = criar_experimento(
        dados=dados_classificacao,
        coluna_alvo='target',
        tipo_problema='classificacao'
    )
    
    assert isinstance(exp, ClassificationExperiment)


def test_criar_experimento_regressao(dados_regressao):
    """Testa criação de experimento de regressão."""
    exp = criar_experimento(
        dados=dados_regressao,
        coluna_alvo='target',
        tipo_problema='regressao'
    )
    
    assert isinstance(exp, RegressionExperiment)


def test_criar_experimento_tipo_invalido(dados_classificacao):
    """Testa que tipo_problema inválido levanta ValueError."""
    with pytest.raises(ValueError, match="tipo_problema deve ser"):
        criar_experimento(
            dados=dados_classificacao,
            coluna_alvo='target',
            tipo_problema='clustering'
        )


def test_criar_experimento_com_params_customizados(dados_classificacao):
    """Testa criação de experimento com parâmetros personalizados."""
    params_custom = {
        'fold': 3,
        'session_id': 123
    }
    
    exp = criar_experimento(
        dados=dados_classificacao,
        coluna_alvo='target',
        tipo_problema='classificacao',
        params=params_custom
    )
    
    assert isinstance(exp, ClassificationExperiment)


def test_criar_experimento_coluna_alvo_inexistente(dados_classificacao):
    """Testa comportamento quando coluna alvo não existe."""
    with pytest.raises(Exception):  # PyCaret levanta exceção
        criar_experimento(
            dados=dados_classificacao,
            coluna_alvo='coluna_inexistente',
            tipo_problema='classificacao'
        )
