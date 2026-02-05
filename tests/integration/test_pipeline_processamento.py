"""
Testes de integração para o pipeline de processamento completo.

Testa o pipeline end-to-end com dados sintéticos para garantir
que todas as etapas funcionem em conjunto.
"""

import numpy as np
import pandas as pd
import pytest

# NOTA: Estes testes usam funções antigas que foram descontinuadas.
# Os testes foram desabilitados. Use test_pipeline_end_to_end.py e test_cenarios_reais.py
# para testes de integração atualizados com a nova estrutura de pipelines.

pytest.skip("Testes antigos descontinuados - usar test_pipeline_end_to_end.py", allow_module_level=True)


class TestPipelineProcessamento:
    """Testes de integração para o pipeline completo de processamento"""

    @pytest.mark.integration
    def test_pipeline_basico_sem_clearml(
        self,
        dados_conforto_termico_basico,
        configuracao_processamento_teste,
        monkeypatch,
    ):
        """Testa pipeline básico sem ClearML"""
        from conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        # Executa o pipeline
        df_processado, artefatos = processar_df(
            dados_conforto_termico_basico, configuracao_processamento_teste
        )

        # Validações básicas
        assert_dataframe_estrutura_valida(df_processado, esperado_min_colunas=3)
        assert isinstance(artefatos, dict)

        # Verifica se algumas transformações básicas foram aplicadas
        assert len(df_processado) == len(dados_conforto_termico_basico)

        # Verifica se colunas de data foram processadas corretamente
        if "data" in df_processado.columns:
            assert df_processado["data"].dtype == "datetime64[ns]"

    @pytest.mark.integration
    def test_pipeline_com_features_derivadas(
        self, dados_conforto_termico_basico, monkeypatch
    ):
        """Testa pipeline com criação de features derivadas"""
        from tests.conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        # Configuração que habilita features derivadas
        cfg = ConfiguracaoProcessamento()
        cfg.criar_features_derivadas = True
        cfg.tipos_features_derivadas = ["imc", "heat_index", "dew_point"]
        cfg.aplicar_normalizacao = False  # Desabilitar para simplificar teste

        df_processado, artefatos = processar_df(dados_conforto_termico_basico, cfg)

        # Verifica se features derivadas foram criadas
        colunas = df_processado.columns.tolist()

        # IMC deve ser criado se peso e altura estiverem presentes
        if (
            "peso" in dados_conforto_termico_basico.columns
            and "altura" in dados_conforto_termico_basico.columns
        ):
            assert "IMC" in colunas

        # Heat index deve ser criado se tmedia e ur estiverem presentes
        if (
            "tmedia" in dados_conforto_termico_basico.columns
            and "ur" in dados_conforto_termico_basico.columns
        ):
            assert "heat_index" in colunas

    @pytest.mark.integration
    def test_pipeline_com_dados_problematicos(self, monkeypatch):
        """Testa pipeline com dados que têm problemas comuns"""
        from tests.conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        # Criar dados com problemas típicos
        dados_problematicos = pd.DataFrame(
            {
                "data": ["2025-01-15", "2025-01-16", None],  # Data nula
                "idade": [25, "x", 35],  # Valor inválido
                "sexo": ["m", "f", ""],  # String vazia
                "peso": [70.5, "65,2", np.nan],  # Vírgula decimal e NaN
                "altura": [175, 160, 180],
                "tmedia": [23.5, 99, 20.1],  # Valor 99 (código de missing)
                "ur": [60, 45, 75],
            }
        )

        # Configuração com limpeza habilitada mas sem imputação
        cfg = ConfiguracaoProcessamento()
        cfg.substituicoes_limpeza = {"x": np.nan, 99: np.nan, "": np.nan}
        cfg.aplicar_normalizacao = False
        cfg.criar_features_derivadas = False
        cfg.metodo_imputacao_numerica = None  # Desabilita imputação para testar limpeza
        cfg.metodo_imputacao_categorica = None

        # Deve processar sem erro
        df_processado, artefatos = processar_df(dados_problematicos, cfg)

        # Validações básicas
        assert_dataframe_estrutura_valida(df_processado, esperado_min_colunas=3)

        # Verifica se limpeza foi aplicada
        # Valor 'x' na idade deve ter virado NaN
        assert pd.isna(df_processado["idade"].iloc[1])

        # Valor 99 na tmedia deve ter sido limpo (pode virar NaN ou ser imputado)
        # Vamos verificar se não é mais 99
        assert df_processado["tmedia"].iloc[1] != 99

    @pytest.mark.integration
    def test_pipeline_com_codificacao(self, dados_conforto_termico_basico, monkeypatch):
        """Testa pipeline com codificação de variáveis categóricas"""
        from tests.conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        cfg = ConfiguracaoProcessamento()
        cfg.aplicar_codificacao = True
        cfg.metodo_codificacao = "label"
        cfg.aplicar_normalizacao = False
        cfg.criar_features_derivadas = False

        df_processado, artefatos = processar_df(dados_conforto_termico_basico, cfg)

        # Verifica se artefatos de codificação foram criados
        assert isinstance(artefatos, dict)

        # Deve ter mapeamentos para variáveis categóricas
        mapas_esperados = [
            chave for chave in artefatos.keys() if chave.startswith("map_")
        ]

        if "sexo" in dados_conforto_termico_basico.columns:
            # Deve existir coluna codificada para sexo
            coluna_sexo_cod = f"sexo{cfg.sufixo_colunas_codificadas}"
            assert coluna_sexo_cod in df_processado.columns

            # Deve existir mapeamento para sexo
            assert any("sexo" in mapa for mapa in mapas_esperados)

    @pytest.mark.integration
    def test_pipeline_dados_grandes(self, dados_conforto_termico_completo, monkeypatch):
        """Testa pipeline com dataset maior"""
        from tests.conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        # Configuração completa mas sem normalização (para acelerar teste)
        cfg = ConfiguracaoProcessamento()
        cfg.aplicar_normalizacao = False

        df_processado, artefatos = processar_df(dados_conforto_termico_completo, cfg)

        # Validações para dataset maior
        assert len(df_processado) == len(dados_conforto_termico_completo)
        assert len(df_processado) == 100  # Confirmando tamanho esperado

        # Deve ter mais colunas devido às transformações
        assert len(df_processado.columns) >= len(
            dados_conforto_termico_completo.columns
        )

        # Não deve ter valores infinitos
        numeric_columns = df_processado.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            assert not np.isinf(
                df_processado[col]
            ).any(), f"Coluna {col} contém valores infinitos"

    @pytest.mark.integration
    @pytest.mark.slow  # Marca como teste lento
    def test_pipeline_todas_opcoes_habilitadas(
        self, dados_conforto_termico_completo, monkeypatch
    ):
        """Testa pipeline com todas as opções habilitadas (teste mais completo e lento)"""
        from tests.conftest import criar_mock_clearml_disponivel

        criar_mock_clearml_disponivel(monkeypatch, disponivel=False)

        # Configuração com todas as features habilitadas
        cfg = ConfiguracaoProcessamento()
        # Mantém configuração padrão (todas as features habilitadas)

        df_processado, artefatos = processar_df(dados_conforto_termico_completo, cfg)

        # Validações extensivas
        assert_dataframe_estrutura_valida(df_processado, esperado_min_colunas=10)

        # Verifica se features temporais foram criadas
        features_temporais_esperadas = ["mes", "ano", "dia_semana", "trimestre"]
        if cfg.criar_features_temporais:
            for feature in features_temporais_esperadas:
                assert (
                    feature in df_processado.columns
                ), f"Feature temporal {feature} não encontrada"

        # Verifica se features derivadas foram criadas
        if cfg.criar_features_derivadas and "imc" in cfg.tipos_features_derivadas:
            assert "IMC" in df_processado.columns, "Feature IMC não encontrada"

        # Verifica se normalização foi aplicada
        if cfg.aplicar_normalizacao:
            colunas_normalizadas = [
                col
                for col in df_processado.columns
                if col.endswith(cfg.sufixo_colunas_normalizadas)
            ]
            assert len(colunas_normalizadas) > 0, "Nenhuma coluna foi normalizada"
