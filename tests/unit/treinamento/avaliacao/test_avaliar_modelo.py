"""
Testes unitários para módulo de avaliação de modelos.
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.treinamento.avaliar_modelo import avaliar_modelo
from src.treinamento.treinar_modelo_base import treinar_modelo_base


class TestAvaliarModelo:
    """Testes para função avaliar_modelo."""
    
    @pytest.fixture
    def modelo_e_dados(self):
        """Cria modelo treinado e dados de teste."""
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.randn(200),
            'feature2': np.random.randn(200),
            'feature3': np.random.randn(200),
        })
        y = pd.Series(np.random.randint(0, 2, 200), name='target')
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        modelo = RandomForestClassifier(n_estimators=10, random_state=42)
        modelo_treinado = treinar_modelo_base(modelo, X_train, y_train)
        
        return modelo_treinado, X_test, y_test
    
    def test_avaliar_modelo_retorna_metricas(self, modelo_e_dados):
        """Verifica se avaliação retorna métricas esperadas."""
        modelo, X_test, y_test = modelo_e_dados
        
        metricas = avaliar_modelo(modelo, X_test, y_test)
        
        assert isinstance(metricas, dict)
        assert 'accuracy' in metricas or 'acuracia' in metricas
    
    def test_metricas_estao_no_intervalo_valido(self, modelo_e_dados):
        """Verifica se métricas estão em intervalos válidos."""
        modelo, X_test, y_test = modelo_e_dados
        
        metricas = avaliar_modelo(modelo, X_test, y_test)
        
        # Métricas devem estar entre 0 e 1
        for chave, valor in metricas.items():
            if isinstance(valor, (int, float)):
                assert 0 <= valor <= 1, f"{chave} fora do intervalo [0,1]: {valor}"
