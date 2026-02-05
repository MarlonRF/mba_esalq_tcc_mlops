"""
Testes unitários para módulo de predições.
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from src.treinamento.fazer_predicoes import fazer_predicoes
from src.treinamento.treinar_modelo_base import treinar_modelo_base


class TestFazerPredicoes:
    """Testes para função fazer_predicoes."""
    
    @pytest.fixture
    def modelo_treinado(self):
        """Cria modelo treinado para testes."""
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100),
        })
        y = pd.Series(np.random.randint(0, 2, 100), name='target')
        
        modelo = RandomForestClassifier(n_estimators=10, random_state=42)
        return treinar_modelo_base(modelo, X, y)
    
    @pytest.fixture
    def dados_novos(self):
        """Cria novos dados para predição."""
        np.random.seed(123)
        return pd.DataFrame({
            'feature1': np.random.randn(20),
            'feature2': np.random.randn(20),
            'feature3': np.random.randn(20),
        })
    
    def test_predicoes_tem_tamanho_correto(self, modelo_treinado, dados_novos):
        """Verifica se número de predições corresponde aos dados de entrada."""
        predicoes = fazer_predicoes(modelo_treinado, dados_novos)
        
        assert len(predicoes) == len(dados_novos)
    
    def test_predicoes_sao_validas(self, modelo_treinado, dados_novos):
        """Verifica se predições são valores válidos (0 ou 1)."""
        predicoes = fazer_predicoes(modelo_treinado, dados_novos)
        
        assert all(p in [0, 1] for p in predicoes)
    
    def test_predicoes_com_probabilidades(self, modelo_treinado, dados_novos):
        """Testa predições com probabilidades se função suportar."""
        try:
            # Tenta obter probabilidades
            probs = modelo_treinado.predict_proba(dados_novos)
            assert probs.shape[0] == len(dados_novos)
            assert probs.shape[1] == 2  # Classificação binária
            assert np.allclose(probs.sum(axis=1), 1.0)  # Soma das probabilidades = 1
        except AttributeError:
            # Modelo não suporta predict_proba
            pytest.skip("Modelo não suporta predict_proba")
