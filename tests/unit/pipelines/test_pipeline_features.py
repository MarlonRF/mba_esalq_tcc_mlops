"""
Testes unitários para o pipeline de features.
"""
import pytest
import pandas as pd
import numpy as np
from src.pipelines.pipeline_features import executar_pipeline_features


@pytest.fixture
def df_processado():
    """DataFrame processado para testes de features."""
    np.random.seed(42)
    return pd.DataFrame({
        'temperatura': np.random.uniform(15, 35, 100),
        'umidade': np.random.uniform(30, 90, 100),
        'peso': np.random.uniform(50, 100, 100),
        'altura': np.random.uniform(1.5, 2.0, 100),
        'sexo': np.random.choice(['m', 'f'], 100),
        'vestimenta': np.random.choice(['leve', 'media', 'pesada'], 100),
        'mes-ano': pd.date_range('2024-01-01', periods=100, freq='D').to_period('M').astype(str),
    })


class TestPipelineFeatures:
    """Testes para o pipeline de features."""
    
    def test_pipeline_basico(self, df_processado):
        """Testa execução básica do pipeline."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=False,
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        assert df_feat.shape == df_processado.shape
        assert isinstance(artefatos, dict)
    
    def test_codificacao_label(self, df_processado):
        """Testa codificação label encoding."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            colunas_categoricas=['sexo', 'vestimenta'],
            aplicar_codificacao=True,
            metodo_codificacao='label',
            sufixo_codificacao='_cod',
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        assert 'sexo_cod' in df_feat.columns
        assert 'vestimenta_cod' in df_feat.columns
        assert 'mapeamentos_codificacao' in artefatos
        assert 'sexo' in artefatos['mapeamentos_codificacao']
        assert df_feat['sexo_cod'].dtype in [np.int64, np.int32]
    
    def test_codificacao_onehot(self, df_processado):
        """Testa codificação one-hot encoding."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            colunas_categoricas=['sexo'],
            aplicar_codificacao=True,
            metodo_codificacao='onehot',
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        assert 'colunas_onehot' in artefatos
        assert len(artefatos['colunas_onehot']) >= 1
        assert df_feat.shape[1] > df_processado.shape[1]
    
    def test_normalizacao_todas_colunas(self, df_processado):
        """Testa normalização de todas as colunas numéricas."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=False,
            aplicar_normalizacao=True,
            metodo_normalizacao='standard',
            sufixo_normalizacao='_norm',
            criar_features_derivadas=False,
        )
        
        assert 'colunas_normalizadas' in artefatos
        assert len(artefatos['colunas_normalizadas']) > 0
        assert 'temperatura_norm' in df_feat.columns
        assert 'umidade_norm' in df_feat.columns
    
    def test_normalizacao_colunas_especificas(self, df_processado):
        """Testa normalização de colunas específicas com métodos diferentes."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=False,
            aplicar_normalizacao=True,
            colunas_normalizar={
                'temperatura': 'standard',
                'umidade': 'minmax'
            },
            sufixo_normalizacao='_norm',
            criar_features_derivadas=False,
        )
        
        assert 'temperatura_norm' in df_feat.columns
        assert 'umidade_norm' in df_feat.columns
        assert 'peso_norm' not in df_feat.columns  # Não deve normalizar
    
    def test_features_derivadas(self, df_processado):
        """Testa criação de features derivadas."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=False,
            aplicar_normalizacao=False,
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc', 't*u'],
        )
        
        assert 'imc' in df_feat.columns
        assert 't*u' in df_feat.columns
        assert df_feat.shape[1] > df_processado.shape[1]
    
    def test_pipeline_completo(self, df_processado):
        """Testa pipeline completo com todas as etapas."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            colunas_categoricas=['sexo', 'vestimenta'],
            aplicar_codificacao=True,
            metodo_codificacao='label',
            aplicar_normalizacao=True,
            metodo_normalizacao='standard',
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc'],
        )
        
        # Deve ter features derivadas
        assert 'imc' in df_feat.columns
        
        # Deve ter codificação
        assert 'sexo_cod' in df_feat.columns
        assert 'mapeamentos_codificacao' in artefatos
        
        # Deve ter normalização
        assert 'colunas_normalizadas' in artefatos
        assert len([c for c in df_feat.columns if c.endswith('_norm')]) > 0
    
    def test_ordem_operacoes(self, df_processado):
        """Testa que features derivadas são criadas antes de codificação/normalização."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=True,
            metodo_codificacao='label',
            colunas_categoricas=['sexo'],
            aplicar_normalizacao=True,
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc'],
        )
        
        # IMC deve existir
        assert 'imc' in df_feat.columns
        
        # IMC também deve ter sido normalizado (se numérico)
        assert any('imc' in c and c.endswith('_norm') for c in df_feat.columns)
    
    def test_preserva_original(self, df_processado):
        """Testa que o DataFrame original não é modificado."""
        df_original = df_processado.copy()
        
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=True,
            aplicar_normalizacao=True,
            criar_features_derivadas=True,
        )
        
        pd.testing.assert_frame_equal(df_processado, df_original)
    
    def test_colunas_inexistentes(self, df_processado):
        """Testa comportamento com colunas que não existem."""
        df_feat, artefatos = executar_pipeline_features(
            df_processado,
            colunas_categoricas=['sexo', 'coluna_inexistente'],
            aplicar_codificacao=True,
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        # Deve processar apenas colunas existentes
        assert 'sexo_cod' in df_feat.columns
        assert 'coluna_inexistente_cod' not in df_feat.columns
