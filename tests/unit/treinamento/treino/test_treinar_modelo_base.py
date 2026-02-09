"""
Testes unitários para módulo de treinamento base.
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.treinamento.treino.treinar_modelo_base import treinar_modelo_base


@pytest.mark.skip(reason="Testes obsoletos - API mudou para usar ClassificationExperiment")
class TestTreinarModeloBase:
    """Testes para função treinar_modelo_base."""
    
    @pytest.fixture
    def dados_treinamento(self):
        """Cria dados de exemplo para treinamento."""
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100),
        })
        y = pd.Series(np.random.randint(0, 2, 100), name='target')
        return X, y
    
    def test_treinar_modelo_basico(self, dados_treinamento):
        """Testa treinamento básico de modelo."""
        X, y = dados_treinamento
        modelo = RandomForestClassifier(n_estimators=10, random_state=42)
        
        modelo_treinado = treinar_modelo_base(modelo, X, y)
        
        assert modelo_treinado is not None
        assert hasattr(modelo_treinado, 'predict')
        assert modelo_treinado.n_estimators == 10
    
    def test_modelo_treinado_faz_predicoes(self, dados_treinamento):
        """Verifica se modelo treinado consegue fazer predições."""
        X, y = dados_treinamento
        modelo = LogisticRegression(random_state=42, max_iter=200)
        
        modelo_treinado = treinar_modelo_base(modelo, X, y)
        predicoes = modelo_treinado.predict(X)
        
        assert len(predicoes) == len(y)
        assert all(p in [0, 1] for p in predicoes)
    
    def test_modelo_com_diferentes_tipos(self, dados_treinamento):
        """Testa treinamento com diferentes tipos de modelos."""
        X, y = dados_treinamento
        
        modelos = [
            RandomForestClassifier(n_estimators=5, random_state=42),
            LogisticRegression(random_state=42, max_iter=200),
        ]
        
        for modelo in modelos:
            modelo_treinado = treinar_modelo_base(modelo, X, y)
            assert modelo_treinado is not None
            assert hasattr(modelo_treinado, 'predict')
