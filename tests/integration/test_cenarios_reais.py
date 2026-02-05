"""
Testes de integração com cenários reais do projeto.

Testa pipelines usando o dataset real de conforto térmico,
validando comportamento com dados reais e edge cases.
"""
import pytest
import pandas as pd
from pathlib import Path

from src.pipelines.pipeline_processamento import executar_pipeline_processamento
from src.pipelines.pipeline_features import executar_pipeline_features
from src.pipelines.pipeline_treinamento_unified import treinar_rapido
from src.utils.io.io_local import load_dataframe
from config import config_custom


# Caminho para dados reais (se existir)
DADOS_REAIS_PATH = Path(__file__).parents[2] / 'dados' / '2025.05.14_thermal_confort_santa_maria_brazil_.csv'


@pytest.mark.integration
@pytest.mark.skipif(not DADOS_REAIS_PATH.exists(), reason="Dados reais não encontrados")
class TestCenarioRealConfortoTermico:
    """Testa pipeline com dataset real de conforto térmico."""
    
    def test_pipeline_com_dados_reais_subset(self):
        """Testa pipeline com subset pequeno dos dados reais."""
        
        # Carrega apenas subset para teste rápido
        df_raw = load_dataframe(str(DADOS_REAIS_PATH))
        df_sample = df_raw.head(100).copy()
        
        # Processamento com configuração real
        df_proc = executar_pipeline_processamento(
            df_sample,
            config_imputacao_customizada=config_custom.CONFIG_IMPUTACAO_CUSTOMIZADA,
            criar_agrupamento_temporal=True,
            nome_coluna_agrupamento='mes-ano'
        )
        
        # Validações
        assert len(df_proc) > 0
        assert 'mes-ano' in df_proc.columns
        
        # Features com configuração real
        df_feat, artefatos = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            metodo_codificacao='label',
            criar_features_derivadas=True,
            tipos_features_derivadas=['imc', 'heat_index', 'dew_point'],
            aplicar_normalizacao=True,
            metodo_normalizacao='standard'
        )
        
        assert len(df_feat) > 0
        assert 'imc' in df_feat.columns
        
        # Treinamento rápido
        features = ['idade', 'sexo_cod', 'peso', 'altura', 'tmedia', 'ur', 'imc']
        target = 'p1'
        
        # Filtra apenas features que existem
        features_existentes = [f for f in features if f in df_feat.columns]
        if target in df_feat.columns and len(features_existentes) >= 3:
            df_treino = df_feat[features_existentes + [target]].dropna()
            
            if len(df_treino) >= 20:  # Mínimo para treinar
                resultado = treinar_rapido(
                    dados=df_treino,
                    coluna_alvo=target,
                    tipo_problema='classificacao',
                    params_setup={'fold': 2, 'verbose': False}
                )
                
                assert resultado is not None
                assert 'melhor_modelo' in resultado


@pytest.mark.integration
class TestCenariosEdgeCases:
    """Testa cenários edge cases e situações limites."""
    
    def test_dados_com_muitos_missings(self):
        """Testa pipeline com alta porcentagem de valores faltantes."""
        import numpy as np
        
        df = pd.DataFrame({
            'idade': [25, np.nan, 35, np.nan, 45, np.nan, 55, np.nan],
            'sexo': ['m', 'f', np.nan, 'm', np.nan, 'f', 'm', np.nan],
            'peso': [70, np.nan, np.nan, 85, np.nan, np.nan, 95, np.nan],
            'altura': [175, 165, np.nan, np.nan, 180, np.nan, np.nan, 170],
            'tmedia': [23, np.nan, 25, np.nan, 22, np.nan, 24, np.nan],
            'target': [0, 1, 0, 1, 0, 1, 0, 1]
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        # Deve processar sem erros, mesmo com muitos NaN
        assert len(df_proc) > 0
        
        # Verifica que imputação foi aplicada
        total_nas_depois = df_proc.isna().sum().sum()
        total_nas_antes = df.isna().sum().sum()
        assert total_nas_depois <= total_nas_antes
    
    
    def test_dados_minimos(self):
        """Testa com quantidade mínima de dados."""
        df = pd.DataFrame({
            'idade': [25, 30, 35, 40, 45],
            'sexo': ['m', 'f', 'm', 'f', 'm'],
            'peso': [70, 65, 80, 60, 85],
            'target': [0, 1, 0, 1, 0]
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        df_feat, _ = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            criar_features_derivadas=False,
            aplicar_normalizacao=False
        )
        
        # Deve processar sem erros
        assert len(df_feat) == 5
        assert 'sexo_cod' in df_feat.columns
    
    
    def test_coluna_categorica_valor_unico(self):
        """Testa comportamento com coluna categórica de valor único."""
        df = pd.DataFrame({
            'idade': [25, 30, 35, 40, 45],
            'sexo': ['m', 'm', 'm', 'm', 'm'],  # Todos masculino
            'peso': [70, 65, 80, 60, 85],
            'target': [0, 1, 0, 1, 0]
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        df_feat, artefatos = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            metodo_codificacao='label'
        )
        
        # Deve processar mesmo com apenas 1 categoria
        assert 'sexo_cod' in df_feat.columns
        assert df_feat['sexo_cod'].nunique() == 1


@pytest.mark.integration
class TestValidacaoArtefatos:
    """Testa que artefatos são criados corretamente."""
    
    def test_artefatos_codificacao_criados(self):
        """Verifica criação de artefatos de codificação."""
        df = pd.DataFrame({
            'categoria1': ['A', 'B', 'C', 'A', 'B'],
            'categoria2': ['X', 'Y', 'X', 'Y', 'X'],
            'numerica': [1, 2, 3, 4, 5]
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        df_feat, artefatos = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            metodo_codificacao='label'
        )
        
        # Verifica artefatos
        assert 'artefatos_codificacao' in artefatos
        assert isinstance(artefatos['artefatos_codificacao'], dict)
        assert len(artefatos['artefatos_codificacao']) > 0
    
    
    def test_artefatos_normalizacao_criados(self):
        """Verifica criação de artefatos de normalização."""
        df = pd.DataFrame({
            'valor1': [10, 20, 30, 40, 50],
            'valor2': [100, 200, 300, 400, 500],
            'categoria': ['A', 'A', 'B', 'B', 'C']
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        df_feat, artefatos = executar_pipeline_features(
            df_proc,
            aplicar_codificacao=True,
            aplicar_normalizacao=True,
            metodo_normalizacao='standard'
        )
        
        # Verifica artefatos
        assert 'artefatos_normalizacao' in artefatos
        assert artefatos['artefatos_normalizacao'] is not None


@pytest.mark.integration
class TestComparacaoClassificacaoRegressao:
    """Compara comportamento entre classificação e regressão."""
    
    def test_mesmo_dataset_ambos_tipos(self):
        """Usa mesmo dataset base para classificação e regressão."""
        import numpy as np
        
        df = pd.DataFrame({
            'f1': np.random.rand(50),
            'f2': np.random.rand(50),
            'f3': np.random.rand(50),
            'target_classe': np.random.randint(0, 2, 50),
            'target_valor': np.random.uniform(0, 10, 50)
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        # Classificação
        df_treino_clf = df_proc[['f1', 'f2', 'f3', 'target_classe']].dropna()
        resultado_clf = treinar_rapido(
            dados=df_treino_clf,
            coluna_alvo='target_classe',
            tipo_problema='classificacao',
            params_setup={'fold': 2, 'verbose': False}
        )
        
        # Regressão
        df_treino_reg = df_proc[['f1', 'f2', 'f3', 'target_valor']].dropna()
        resultado_reg = treinar_rapido(
            dados=df_treino_reg,
            coluna_alvo='target_valor',
            tipo_problema='regressao',
            params_setup={'fold': 2, 'verbose': False}
        )
        
        # Ambos devem funcionar
        assert resultado_clf['tipo_problema'] == 'classificacao'
        assert resultado_reg['tipo_problema'] == 'regressao'
        assert 'tabela_comparacao' in resultado_clf
        assert 'tabela_comparacao' in resultado_reg
