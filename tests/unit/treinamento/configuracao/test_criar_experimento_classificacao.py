"""
Testes unitários para funções core de treinamento.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.datasets import make_classification


class TestTreinarModeloBase:
    """Testes para treinar_modelo_base."""
    
    @pytest.fixture
    def dataset_classificacao(self):
        """Cria dataset de classificação simples."""
        X, y = make_classification(
            n_samples=100,
            n_features=5,
            n_informative=3,
            n_redundant=0,
            random_state=42
        )
        df = pd.DataFrame(X, columns=[f'feat{i}' for i in range(5)])
        df['target'] = y
        return df
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_treina_modelo_basico(self, dataset_classificacao):
        """Testa treinamento de modelo base."""
        from src.treinamento import criar_experimento_classificacao, treinar_modelo_base
        
        # Cria experimento
        exp = criar_experimento_classificacao(
            dados=dataset_classificacao,
            coluna_alvo='target'
        )
        
        # Treina modelos base
        modelos, tabela = treinar_modelo_base(
            exp=exp,
            n_select=1,
            include=['dt']
        )
        
        assert modelos is not None
        assert len(modelos) > 0
        assert tabela is not None
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_treina_com_parametros(self, dataset_classificacao):
        """Testa treinamento com parâmetros customizados."""
        from src.treinamento import criar_experimento_classificacao, treinar_modelo_base
        
        # Cria experimento com parâmetros
        exp = criar_experimento_classificacao(
            dados=dataset_classificacao,
            coluna_alvo='target',
            params={'fold': 2, 'session_id': 42}
        )
        
        modelos, tabela = treinar_modelo_base(
            exp=exp,
            n_select=1,
            include=['rf']
        )
        
        assert modelos is not None


class TestOtimizarModelo:
    """Testes para otimizar_modelo."""
    
    @pytest.fixture
    def dataset_classificacao(self):
        """Cria dataset de classificação simples."""
        X, y = make_classification(
            n_samples=100,
            n_features=5,
            n_informative=3,
            random_state=42
        )
        df = pd.DataFrame(X, columns=[f'feat{i}' for i in range(5)])
        df['target'] = y
        return df
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_otimiza_modelo(self, dataset_classificacao):
        """Testa otimização de hiperparâmetros."""
        from src.treinamento import (
            criar_experimento_classificacao,
            treinar_modelo_base,
            otimizar_modelo
        )
        
        # Cria experimento
        exp = criar_experimento_classificacao(
            dados=dataset_classificacao,
            coluna_alvo='target'
        )
        
        # Primeiro treina modelo base
        modelos, _ = treinar_modelo_base(
            exp=exp,
            n_select=1,
            include=['dt']
        )
        
        # Otimiza
        modelo_otimizado, metricas = otimizar_modelo(
            exp=exp,
            modelo=modelos[0],
            n_iter=2
        )
        
        assert modelo_otimizado is not None
        assert metricas is not None


class TestFinalizarModelo:
    """Testes para finalizar_modelo."""
    
    @pytest.fixture
    def dataset_classificacao(self):
        """Cria dataset de classificação simples."""
        X, y = make_classification(
            n_samples=100,
            n_features=5,
            n_informative=3,
            random_state=42
        )
        df = pd.DataFrame(X, columns=[f'feat{i}' for i in range(5)])
        df['target'] = y
        return df
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_finaliza_modelo(self, dataset_classificacao):
        """Testa finalização do modelo."""
        from src.treinamento import (
            criar_experimento_classificacao,
            treinar_modelo_base,
            finalizar_modelo
        )
        
        # Cria experimento
        exp = criar_experimento_classificacao(
            dados=dataset_classificacao,
            coluna_alvo='target'
        )
        
        # Treina modelo base
        modelos, _ = treinar_modelo_base(
            exp=exp,
            n_select=1,
            include=['dt']
        )
        
        # Finaliza
        modelo_final = finalizar_modelo(exp, modelos[0])
        
        assert modelo_final is not None


class TestFazerPredicoes:
    """Testes para fazer_predicoes."""
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_predicoes_basicas(self):
        """Testa predições básicas."""
        from src.treinamento import (
            criar_experimento_classificacao,
            treinar_modelo_base,
            fazer_predicoes
        )
        
        # Dataset simples
        dados = pd.DataFrame({
            'feat1': [1, 2, 3, 4, 5],
            'feat2': [5, 4, 3, 2, 1],
            'target': [0, 0, 1, 1, 1]
        })
        
        # Cria experimento e treina
        exp = criar_experimento_classificacao(
            dados=dados,
            coluna_alvo='target'
        )
        
        modelos, _ = treinar_modelo_base(exp, n_select=1, include=['dt'])
        
        # Faz predições
        predicoes_df = fazer_predicoes(exp, modelos[0], dados)
        
        assert len(predicoes_df) == 5
        assert 'prediction_label' in predicoes_df.columns


class TestAvaliarModelo:
    """Testes para avaliar_modelo."""
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_avalia_modelo(self):
        """Testa avaliação de modelo."""
        from src.treinamento import (
            criar_experimento_classificacao,
            treinar_modelo_base,
            avaliar_modelo
        )
        
        # Dataset simples
        dados = pd.DataFrame({
            'feat1': [1, 2, 3, 4, 5, 6, 7, 8],
            'feat2': [5, 4, 3, 2, 1, 5, 4, 3],
            'target': [0, 0, 1, 1, 1, 0, 0, 1]
        })
        
        # Cria experimento
        exp = criar_experimento_classificacao(
            dados=dados,
            coluna_alvo='target'
        )
        
        # Treina
        modelos, _ = treinar_modelo_base(exp, n_select=1, include=['dt'])
        
        # Avalia
        resultado = avaliar_modelo(
            exp=exp,
            modelo=modelos[0],
            dados_teste=dados,
            coluna_alvo='target'
        )
        
        assert isinstance(resultado, dict)
        assert 'metricas' in resultado
        assert 'accuracy' in resultado['metricas']


class TestSalvarCarregarModelo:
    """Testes para salvar e carregar modelo."""
    
    @pytest.mark.skip(reason="Requer experimento PyCaret configurado")
    def test_salva_e_carrega(self, tmp_path):
        """Testa salvamento e carregamento de modelo."""
        from src.treinamento import (
            criar_experimento_classificacao,
            treinar_modelo_base,
            salvar_modelo,
            carregar_modelo
        )
        
        # Dataset simples
        dados = pd.DataFrame({
            'feat1': [1, 2, 3, 4, 5],
            'feat2': [5, 4, 3, 2, 1],
            'target': [0, 0, 1, 1, 1]
        })
        
        # Cria experimento e treina
        exp = criar_experimento_classificacao(
            dados=dados,
            coluna_alvo='target'
        )
        
        modelos, _ = treinar_modelo_base(exp, n_select=1, include=['dt'])
        
        # Salva
        caminho = salvar_modelo(
            exp=exp,
            modelo=modelos[0],
            nome_modelo="test_model",
            pasta_destino=str(tmp_path)
        )
        
        assert Path(caminho).exists()
        
        # Carrega
        modelo_carregado = carregar_modelo(caminho)
        
        assert modelo_carregado is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
