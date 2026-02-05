"""
Testes unitários para funções utilitárias de treinamento.
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


class TestExtrairEstimador:
    """Testes para extrair_estimador."""
    
    def test_extrai_estimador_sklearn(self):
        """Testa extração de estimador sklearn."""
        from src.treinamento import extrair_estimador
        
        modelo = RandomForestClassifier(random_state=42)
        estimador = extrair_estimador(modelo)
        
        assert estimador is modelo
        assert isinstance(estimador, RandomForestClassifier)
    
    def test_extrai_estimador_pycaret(self):
        """Testa extração de estimador de objeto PyCaret."""
        from src.treinamento import extrair_estimador
        
        # Simula objeto PyCaret com atributo estimator
        class MockPyCaretModel:
            def __init__(self):
                self.estimator = DecisionTreeClassifier()
        
        modelo_pycaret = MockPyCaretModel()
        estimador = extrair_estimador(modelo_pycaret)
        
        assert estimador is modelo_pycaret.estimator
        assert isinstance(estimador, DecisionTreeClassifier)


class TestExtrairInfoModelo:
    """Testes para extrair_info_modelo."""
    
    def test_extrai_info_basica(self):
        """Testa extração de informações básicas do modelo."""
        from src.treinamento import extrair_info_modelo
        
        modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        info = extrair_info_modelo(modelo)
        
        assert "modelo_nome" in info
        assert info["modelo_nome"] == "RandomForestClassifier"
        assert "parametros" in info
        assert info["parametros"]["n_estimators"] == 100
        assert info["parametros"]["max_depth"] == 10


class TestClassificarMetricas:
    """Testes para classificar_metricas."""
    
    def test_classifica_metricas_ranking(self):
        """Testa classificação/ranking de modelos por múltiplas métricas."""
        from src.treinamento import classificar_metricas
        
        # Cria DataFrame com métricas de múltiplos modelos
        tabela = pd.DataFrame({
            "Model": ["rf", "lr", "dt"],
            "Accuracy": [0.85, 0.80, 0.82],
            "F1": [0.83, 0.78, 0.81],
            "AUC": [0.90, 0.85, 0.87]
        })
        
        # Classifica por múltiplas métricas
        resultado = classificar_metricas(tabela, ["Accuracy", "F1", "AUC"])
        
        assert "classificacao_Accuracy" in resultado.columns
        assert "classificacao_F1" in resultado.columns
        assert "classificacao_media" in resultado.columns
        assert resultado["classificacao_Accuracy"].iloc[0] == 1  # rf é o melhor
    
    def test_metricas_inexistentes(self):
        """Testa comportamento com métricas inexistentes."""
        from src.treinamento import classificar_metricas
        
        tabela = pd.DataFrame({"Model": ["rf"], "Accuracy": [0.85]})
        
        with pytest.raises(ValueError):
            classificar_metricas(tabela, ["MetricaInexistente"])


class TestExtrairImportanciaFeatures:
    """Testes para extrair_importancia_features."""
    
    def test_extrai_importancia_rf(self):
        """Testa extração de importância de features de Random Forest."""
        from src.treinamento import extrair_importancia_features
        
        # Dados de treino simples
        dados = pd.DataFrame({
            'feat1': [1, 2, 3, 4, 5],
            'feat2': [5, 4, 3, 2, 1],
            'feat3': [2, 2, 2, 2, 2],
            'target': [0, 0, 1, 1, 1]
        })
        
        # Extrai importâncias (função treina o RF internamente)
        resultado = extrair_importancia_features(
            dados=dados,
            coluna_alvo='target',
            atributos=['feat1', 'feat2', 'feat3']
        )
        
        assert isinstance(resultado, dict)
        assert 'importancias' in resultado
        assert 'modelo' in resultado
        importancias_df = resultado['importancias']
        assert 'feature' in importancias_df.columns
        assert 'importancia' in importancias_df.columns
        assert len(importancias_df) == 3
        assert all(importancias_df['importancia'] >= 0)
    
    def test_top_n_features(self):
        """Testa extração de top N features mais importantes."""
        from src.treinamento import extrair_importancia_features
        
        dados = pd.DataFrame({
            'feat1': [1, 2, 3, 4, 5],
            'feat2': [5, 4, 3, 2, 1],
            'feat3': [2, 2, 2, 2, 2],
            'target': [0, 0, 1, 1, 1]
        })
        
        resultado = extrair_importancia_features(
            dados=dados,
            coluna_alvo='target',
            n_top_features=2
        )
        
        assert 'top_features' in resultado
        assert len(resultado['top_features']) == 2


class TestSalvarPlotsModelo:
    """Testes para salvar_plots_modelo."""
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_salva_plots_pycaret(self, tmp_path):
        """Testa salvamento de plots com PyCaret real."""
        from src.treinamento import salvar_plots_modelo
        # Este teste requer um experimento PyCaret real
        # Pulado por enquanto - testar em teste de integração
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
