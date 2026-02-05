"""
Testes de integração end-to-end: Processamento → Features → Treinamento

Este arquivo testa o fluxo completo do MLOps pipeline:
1. Pipeline de processamento (limpeza + imputação + temporal)
2. Pipeline de features (codificação + derivadas + normalização)
3. Pipeline de treinamento (classificação e regressão)
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.pipelines.pipeline_processamento import executar_pipeline_processamento
from src.pipelines.pipeline_features import executar_pipeline_features
from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo, treinar_rapido
from config.config_gerais import PARAMS_PADRAO


@pytest.fixture
def dados_brutos_completos():
    """Dataset sintético simulando dados reais do projeto."""
    np.random.seed(42)
    n_samples = 100
    
    return pd.DataFrame({
        # Dados pessoais
        'idade': np.random.randint(18, 70, n_samples),
        'sexo': np.random.choice(['m', 'f'], n_samples),
        'peso': np.random.uniform(50, 100, n_samples),
        'altura': np.random.uniform(150, 190, n_samples),
        
        # Dados ambientais
        'tmedia': np.random.uniform(18, 35, n_samples),
        'ur': np.random.uniform(40, 90, n_samples),
        'vel_vento': np.random.uniform(0, 15, n_samples),
        
        # Target para classificação
        'target_classe': np.random.randint(0, 3, n_samples),
        
        # Target para regressão
        'target_valor': np.random.uniform(0, 10, n_samples),
        
        # Alguns valores missing
        'feature_missing': [np.nan if i % 10 == 0 else i for i in range(n_samples)]
    })


@pytest.mark.integration
class TestFluxoCompletoClassificacao:
    """Testa pipeline completo end-to-end para classificação."""
    
    def test_pipeline_completo_classificacao(self, dados_brutos_completos):
        """Testa fluxo: dados brutos → processamento → features → treinamento (classificação)."""
        
        # ETAPA 1: Processamento
        df_processado = executar_pipeline_processamento(
            dados_brutos_completos,
            criar_agrupamento_temporal=False  # Dados sintéticos sem temporal
        )
        
        assert len(df_processado) > 0
        assert 'sexo' in df_processado.columns
        
        # ETAPA 2: Features
        df_features, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=True,
            metodo_codificacao='label',
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc'],
            aplicar_normalizacao=True,
            metodo_normalizacao='standard'
        )
        
        assert len(df_features) == len(df_processado)
        assert 'sexo_cod' in df_features.columns  # Codificado
        assert 'imc' in df_features.columns  # Feature derivada
        assert 'artefatos_codificacao' in artefatos
        
        # ETAPA 3: Treinamento (classificação)
        features_treino = ['idade', 'sexo_cod', 'peso', 'altura', 'tmedia', 'ur', 'imc']
        df_treino = df_features[features_treino + ['target_classe']].dropna()
        
        resultado = treinar_rapido(
            dados=df_treino,
            coluna_alvo='target_classe',
            tipo_problema='classificacao',
            params_setup={'fold': 2, 'verbose': False}
        )
        
        # Validações finais
        assert 'experimento' in resultado
        assert 'modelos_base' in resultado
        assert 'tabela_comparacao' in resultado
        assert 'melhor_modelo' in resultado
        assert resultado['tipo_problema'] == 'classificacao'
        assert resultado['tabela_comparacao'] is not None


@pytest.mark.integration
class TestFluxoCompletoRegressao:
    """Testa pipeline completo end-to-end para regressão."""
    
    def test_pipeline_completo_regressao(self, dados_brutos_completos):
        """Testa fluxo: dados brutos → processamento → features → treinamento (regressão)."""
        
        # ETAPA 1: Processamento
        df_processado = executar_pipeline_processamento(
            dados_brutos_completos,
            criar_agrupamento_temporal=False
        )
        
        assert len(df_processado) > 0
        
        # ETAPA 2: Features (mínimas para teste rápido)
        df_features, artefatos = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=True,
            metodo_codificacao='label',
            criar_features_derivadas=False,  # Desabilita para ser mais rápido
            aplicar_normalizacao=False
        )
        
        assert len(df_features) > 0
        
        # ETAPA 3: Treinamento (regressão)
        features_treino = ['idade', 'sexo_cod', 'peso', 'altura', 'tmedia', 'ur']
        df_treino = df_features[features_treino + ['target_valor']].dropna()
        
        resultado = treinar_rapido(
            dados=df_treino,
            coluna_alvo='target_valor',
            tipo_problema='regressao',
            params_setup={'fold': 2, 'verbose': False}
        )
        
        # Validações
        assert resultado['tipo_problema'] == 'regressao'
        assert 'melhor_modelo' in resultado
        assert resultado['tabela_comparacao'] is not None


@pytest.mark.integration
@pytest.mark.slow
class TestFluxoCompletoComOtimizacao:
    """Testa pipeline completo com otimização de hiperparâmetros (mais lento)."""
    
    def test_pipeline_com_otimizacao_classificacao(self, dados_brutos_completos):
        """Testa pipeline completo com otimização para classificação."""
        
        # Pipeline rápido
        df_processado = executar_pipeline_processamento(
            dados_brutos_completos,
            criar_agrupamento_temporal=False
        )
        
        df_features, _ = executar_pipeline_features(
            df_processado,
            aplicar_codificacao=True,
            metodo_codificacao='label',
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc'],
            aplicar_normalizacao=False
        )
        
        # Treinamento COM otimização
        features_treino = ['idade', 'sexo_cod', 'peso', 'imc', 'tmedia']
        df_treino = df_features[features_treino + ['target_classe']].dropna()
        
        resultado = treinar_pipeline_completo(
            dados=df_treino,
            coluna_alvo='target_classe',
            tipo_problema='classificacao',
            params_setup={'fold': 2, 'verbose': False},
            n_modelos_comparar=2,
            otimizar_hiperparametros=True,
            n_iter_otimizacao=3,  # Poucas iterações para teste
            finalizar=False,  # Não finaliza para ser mais rápido
            salvar_modelo_final=False
        )
        
        # Validações
        assert 'modelo_otimizado' in resultado
        assert resultado['modelo_otimizado'] is not None
        assert 'metricas_melhor' in resultado


@pytest.mark.integration
class TestConsistenciaDados:
    """Testa consistência dos dados através do pipeline."""
    
    def test_sem_perda_excessiva_de_dados(self, dados_brutos_completos):
        """Verifica que não há perda excessiva de dados no pipeline."""
        
        n_original = len(dados_brutos_completos)
        
        # Processamento
        df_proc = executar_pipeline_processamento(
            dados_brutos_completos,
            criar_agrupamento_temporal=False
        )
        
        # Deve manter pelo menos 80% dos dados após processamento
        assert len(df_proc) >= 0.8 * n_original
        
        # Features
        df_feat, _ = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc'],
            aplicar_normalizacao=True
        )
        
        # Não deve perder linhas na engenharia de features
        assert len(df_feat) == len(df_proc)
    
    
    def test_tipos_colunas_consistentes(self, dados_brutos_completos):
        """Verifica que tipos de dados são mantidos consistentemente."""
        
        df_proc = executar_pipeline_processamento(
            dados_brutos_completos,
            criar_agrupamento_temporal=False
        )
        
        df_feat, _ = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            aplicar_normalizacao=True
        )
        
        # Colunas codificadas devem ser numéricas
        if 'sexo_cod' in df_feat.columns:
            assert pd.api.types.is_numeric_dtype(df_feat['sexo_cod'])
        
        # Features numéricas devem permanecer numéricas
        assert pd.api.types.is_numeric_dtype(df_feat['idade'])
        assert pd.api.types.is_numeric_dtype(df_feat['peso'])
