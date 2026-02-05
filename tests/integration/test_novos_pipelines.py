"""
Testes de integração para os novos pipelines modulares.

Testa:
- pipeline_processamento (base)
- pipeline_features (engenharia)
- pipeline_completo (ambos)
"""
import numpy as np
import pandas as pd
import pytest

# NOTA: Estes testes foram criados para uma versão anterior da API dos pipelines.
# Foram desabilitados temporariamente. Use test_pipeline_end_to_end.py para testes atualizados.

pytest.skip("Testes antigos - API dos pipelines mudou - usar test_pipeline_end_to_end.py", allow_module_level=True)


class TestPipelineProcessamentoNovo:
    """Testes para pipeline de processamento base (novo)"""

    def test_pipeline_basico_com_dados_simples(self):
        """Testa pipeline básico com dados simples"""
        df = pd.DataFrame({
            'data': ['15/01/2025', '16/01/2025', '17/01/2025'],
            'hora': ['10:00', '11:00', '12:00'],
            'idade': [25, np.nan, 35],
            'sexo': ['m', 'f', 'm'],
            'peso': [70.0, 80.0, np.nan],
            'altura': [175, 165, 180],
            'tmedia': [23.5, 25.0, 22.0],
            'ur': [60, 65, 70],
        })
        
        df_proc = executar_pipeline_processamento(df)
        
        # Verificações básicas
        assert len(df_proc) == len(df)
        assert df_proc['data'].dtype == 'datetime64[ns]'
        
        # Imputação deve ter sido aplicada
        assert df_proc['idade'].notna().all()
        assert df_proc['peso'].notna().all()

    def test_pipeline_com_config_imputacao_customizada(self):
        """Testa pipeline com configuração customizada de imputação"""
        df = pd.DataFrame({
            'p5': [1, np.nan, 3, 4],
            'p6': [10, np.nan, np.nan, 40],
            'idade': [25, np.nan, 35, 40],
            'peso': [70, np.nan, 80, 75],
        })
        
        config_imput = {
            'p5': 'backward',
            'p6': 'backward',
            'idade': 'median',
            'peso': 'mean',
        }
        
        df_proc = executar_pipeline_processamento(
            df,
            config_imputacao_customizada=config_imput
        )
        
        # p5 deve usar backward fill
        assert df_proc['p5'].iloc[1] == 3
        
        # p6 deve usar backward fill
        assert df_proc['p6'].iloc[1] == 40
        assert df_proc['p6'].iloc[2] == 40
        
        # idade deve usar mediana
        assert df_proc['idade'].iloc[1] == 32.5
        
        # peso deve usar média
        assert df_proc['peso'].iloc[1] == 75.0

    def test_pipeline_com_media_movel(self):
        """Testa pipeline com média móvel + interpolação"""
        valores_radiacao = [100, 110, 120] + [np.nan] * 5 + [180, 190, 200]
        
        df = pd.DataFrame({
            'rsolartot': valores_radiacao,
        })
        
        config_imput = {
            'rsolartot': 'rolling_mean_48',
        }
        
        df_proc = executar_pipeline_processamento(
            df,
            config_imputacao_customizada=config_imput
        )
        
        # Valores devem estar preenchidos
        assert df_proc['rsolartot'].notna().all()
        
        # Valores imputados devem estar em uma faixa razoável
        assert df_proc['rsolartot'].min() >= 100
        assert df_proc['rsolartot'].max() <= 200

    def test_pipeline_com_config_projeto(self):
        """Testa pipeline usando CONFIG_IMPUTACAO_CUSTOMIZADA do config.py"""
        df = pd.DataFrame({
            'p5': [1, np.nan, 3],
            'p6': [10, np.nan, 30],
            'p7': [100, np.nan, 300],
            'p8': [1000, np.nan, 3000],
            'vestimenta': ['leve', np.nan, 'pesada'],
            'idade': [25, np.nan, 35],
        })
        
        df_proc = executar_pipeline_processamento(
            df,
            config_imputacao_customizada=config.CONFIG_IMPUTACAO_CUSTOMIZADA
        )
        
        # Verificar que configurações foram aplicadas
        assert df_proc['p5'].notna().all()  # backward
        assert df_proc['p6'].notna().all()  # backward
        assert df_proc['p7'].notna().all()  # backward
        assert df_proc['p8'].notna().all()  # backward
        assert df_proc['vestimenta'].notna().all()  # backward
        assert df_proc['idade'].notna().all()  # median

    def test_pipeline_cria_agrupamento_temporal(self):
        """Testa que pipeline cria coluna de agrupamento temporal"""
        df = pd.DataFrame({
            'data': ['15/01/2025', '16/02/2025', '17/03/2025'],
            'hora': ['10:00', '11:00', '12:00'],
        })
        
        df_proc = executar_pipeline_processamento(
            df,
            criar_agrupamento_temporal=True,
            nome_coluna_agrupamento='mes-ano'
        )
        
        # Deve ter criado coluna mes-ano
        assert 'mes-ano' in df_proc.columns


class TestPipelineFeatures:
    """Testes para pipeline de features"""

    @pytest.mark.skip(reason="Requer sklearn funcionando")
    def test_pipeline_features_codificacao(self):
        """Testa pipeline de features com codificação"""
        df = pd.DataFrame({
            'sexo': ['m', 'f', 'm', 'f'],
            'vestimenta': ['leve', 'media', 'pesada', 'leve'],
            'idade': [25, 30, 35, 40],
        })
        
        df_feat, artefatos = executar_pipeline_features(
            df,
            colunas_categoricas=['sexo', 'vestimenta'],
            aplicar_codificacao=True,
            metodo_codificacao='label',
            aplicar_normalizacao=False,
        )
        
        # Deve ter colunas codificadas
        assert 'sexo_cod' in df_feat.columns
        assert 'vestimenta_cod' in df_feat.columns
        
        # Deve ter mapeamentos nos artefatos
        assert 'mapeamentos_codificacao' in artefatos

    @pytest.mark.skip(reason="Requer sklearn funcionando")
    def test_pipeline_features_normalizacao(self):
        """Testa pipeline de features com normalização"""
        df = pd.DataFrame({
            'tev': [20.0, 25.0, 30.0, 35.0],
            'utci': [15.0, 20.0, 25.0, 30.0],
        })
        
        df_feat, artefatos = executar_pipeline_features(
            df,
            aplicar_codificacao=False,
            aplicar_normalizacao=True,
            metodo_normalizacao='minmax',
            sufixo_normalizacao='_norm',
        )
        
        # Deve ter colunas normalizadas
        assert 'tev_norm' in df_feat.columns
        assert 'utci_norm' in df_feat.columns
        
        # Valores normalizados devem estar entre 0 e 1
        assert df_feat['tev_norm'].min() >= 0
        assert df_feat['tev_norm'].max() <= 1


class TestPipelineCompleto:
    """Testes para pipeline completo (processamento + features)"""

    def test_pipeline_completo_basico(self):
        """Testa pipeline completo com dados básicos"""
        df = pd.DataFrame({
            'data': ['15/01/2025', '16/01/2025', '17/01/2025'],
            'hora': ['10:00', '11:00', '12:00'],
            'idade': [25, np.nan, 35],
            'sexo': ['m', 'f', 'm'],
            'peso': [70.0, 80.0, np.nan],
            'altura': [175, 165, 180],
        })
        
        df_final, artefatos = executar_pipeline_completo(
            df,
            aplicar_codificacao=False,  # Desabilita para não depender de sklearn
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        # Verificações básicas
        assert len(df_final) == len(df)
        assert df_final['data'].dtype == 'datetime64[ns]'
        
        # Imputação deve ter sido aplicada
        assert df_final['idade'].notna().all()
        assert df_final['peso'].notna().all()
        
        # Deve ter artefatos
        assert isinstance(artefatos, dict)

    def test_pipeline_completo_com_todas_etapas_exceto_sklearn(self):
        """Testa pipeline completo sem features que dependem de sklearn"""
        df = pd.DataFrame({
            'data': ['15/01/2025'] * 5,
            'hora': ['10:00', '11:00', '12:00', '13:00', '14:00'],
            'idade': [25, np.nan, 35, 40, 45],
            'sexo': ['m', 'f', 'm', 'f', 'm'],
            'peso': [70.0, 80.0, np.nan, 75.0, 85.0],
            'altura': [175, 165, 180, 170, 185],
            'p5': [1, np.nan, 3, 4, 5],
            'p6': [10, np.nan, 30, 40, 50],
        })
        
        config_imput = {
            'p5': 'backward',
            'p6': 'backward',
            'idade': 'median',
            'peso': 'mean',
        }
        
        df_final, artefatos = executar_pipeline_completo(
            df,
            config_imputacao_customizada=config_imput,
            criar_agrupamento_temporal=True,
            aplicar_codificacao=False,
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        # Fase de processamento
        assert df_final['data'].dtype == 'datetime64[ns]'
        assert df_final['idade'].notna().all()
        assert df_final['peso'].notna().all()
        assert df_final['p5'].notna().all()
        assert df_final['p6'].notna().all()
        
        # Agrupamento temporal
        assert 'mes-ano' in df_final.columns

    def test_pipeline_completo_shape_final(self):
        """Testa que pipeline não perde linhas"""
        df = pd.DataFrame({
            'data': ['15/01/2025'] * 10,
            'hora': [f'{10+i}:00' for i in range(10)],
            'idade': list(range(20, 30)),
            'peso': list(range(60, 70)),
        })
        
        df_final, artefatos = executar_pipeline_completo(
            df,
            aplicar_codificacao=False,
            aplicar_normalizacao=False,
            criar_features_derivadas=False,
        )
        
        # Não deve perder linhas
        assert len(df_final) == len(df)
        
        # Deve ter pelo menos as colunas originais (pode ter mais por transformações)
        assert len(df_final.columns) >= len(df.columns)


class TestPipelineCompatibilidadeComAntigo:
    """Testes para verificar compatibilidade com comportamento do pipeline antigo"""

    def test_backward_fill_questionario(self):
        """Testa que p5-p8 usam backward fill como no pipeline antigo"""
        df = pd.DataFrame({
            'p5': [1, np.nan, np.nan, 4],
            'p6': [10, np.nan, np.nan, 40],
            'p7': [100, np.nan, np.nan, 400],
            'p8': [1000, np.nan, np.nan, 4000],
        })
        
        df_proc = executar_pipeline_processamento(
            df,
            config_imputacao_customizada=config.CONFIG_IMPUTACAO_CUSTOMIZADA
        )
        
        # Verificar backward fill para todas as perguntas
        assert df_proc['p5'].iloc[1] == 4
        assert df_proc['p5'].iloc[2] == 4
        assert df_proc['p6'].iloc[1] == 40
        assert df_proc['p7'].iloc[1] == 400
        assert df_proc['p8'].iloc[1] == 4000

    def test_backward_fill_vestimenta(self):
        """Testa que vestimenta usa backward fill como no pipeline antigo"""
        df = pd.DataFrame({
            'vestimenta': ['leve', np.nan, np.nan, 'pesada'],
        })
        
        df_proc = executar_pipeline_processamento(
            df,
            config_imputacao_customizada=config.CONFIG_IMPUTACAO_CUSTOMIZADA
        )
        
        # Verificar backward fill
        assert df_proc['vestimenta'].iloc[1] == 'pesada'
        assert df_proc['vestimenta'].iloc[2] == 'pesada'
