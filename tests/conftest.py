"""
Fixtures e utilitários compartilhados para testes.

Este módulo contém fixtures do pytest, dados de teste sintéticos
e funções auxiliares usadas em múltiplos testes.
"""

from typing import Any, Dict

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def dados_conforto_termico_basico():
    """
    Fixture com dados sintéticos básicos de conforto térmico.

    Returns:
        pd.DataFrame: DataFrame com dados mínimos para teste
    """
    return pd.DataFrame(
        {
            "data": ["2025-01-15", "2025-01-16", "2025-01-17"],
            "hora": ["09:00", "14:00", "18:00"],
            "idade": [25, 30, 35],
            "sexo": ["m", "f", "m"],
            "peso": [70, 65, 80],
            "altura": [175, 160, 180],
            "tmedia": [23.5, 28.2, 20.1],
            "ur": [60, 45, 75],
            "vel_vento": [1.2, 0.8, 2.1],
            "p1": [3, 4, 2],  # Escala de conforto
            "p2": [3, 5, 2],
            "p3": [4, 4, 3],
        }
    )


@pytest.fixture
def dados_conforto_termico_completo():
    """
    Fixture com dados sintéticos mais completos para testes de integração.

    Returns:
        pd.DataFrame: DataFrame com dados completos para teste
    """
    np.random.seed(42)  # Para reproducibilidade
    n_samples = 100

    # Gerar datas sequenciais
    dates = pd.date_range("2024-01-01", periods=n_samples, freq="D")

    return pd.DataFrame(
        {
            "data": dates.strftime("%Y-%m-%d"),
            "hora": np.random.choice(["09:00", "12:00", "15:00", "18:00"], n_samples),
            "idade": np.random.randint(18, 65, n_samples),
            "sexo": np.random.choice(["m", "f"], n_samples),
            "peso": np.random.normal(70, 15, n_samples).round(1),
            "altura": np.random.normal(170, 10, n_samples).round(0),
            "tmedia": np.random.normal(25, 5, n_samples).round(1),
            "tmax": np.random.normal(30, 6, n_samples).round(1),
            "tmin": np.random.normal(20, 4, n_samples).round(1),
            "ur": np.random.uniform(30, 90, n_samples).round(1),
            "vel_vento": np.random.exponential(1.5, n_samples).round(1),
            "p1": np.random.randint(1, 8, n_samples),  # Escala Likert 1-7
            "p2": np.random.randint(1, 8, n_samples),
            "p3": np.random.randint(1, 8, n_samples),
            "p4": np.random.randint(1, 8, n_samples),
            "p5": np.random.randint(1, 8, n_samples),
            "vestimenta": np.random.choice(["leve", "normal", "pesada"], n_samples),
        }
    )


@pytest.fixture
def configuracao_processamento_teste():
    """
    Configuração básica para testes de processamento.

    Returns:
        ConfiguracaoProcessamento: Instância configurada para testes
    """
    from utils.processamento import ConfiguracaoProcessamento
    
    cfg = ConfiguracaoProcessamento()
    cfg.substituicoes_limpeza = {"x": np.nan, "99": np.nan}
    cfg.metodo_imputacao_numerica = "median"
    cfg.metodo_imputacao_categorica = "mode"
    cfg.criar_features_temporais = True
    cfg.criar_features_derivadas = True
    cfg.tipos_features_derivadas = ["imc", "heat_index"]
    cfg.aplicar_codificacao = True
    cfg.metodo_codificacao = "label"
    cfg.aplicar_normalizacao = False  # Desabilitar para testes mais simples
    
    return cfg


@pytest.fixture
def arquivo_csv_temporario(tmp_path, dados_conforto_termico_basico):
    """
    Cria arquivo CSV temporário para testes de I/O.

    Args:
        tmp_path: Fixture do pytest para diretório temporário
        dados_conforto_termico_basico: Fixture com dados de teste

    Returns:
        str: Caminho para arquivo CSV temporário
    """
    arquivo = tmp_path / "dados_teste.csv"
    dados_conforto_termico_basico.to_csv(arquivo, index=False)
    return str(arquivo)


def criar_mock_clearml_disponivel(monkeypatch, disponivel: bool = True):
    """
    Utilitário para mockar disponibilidade do ClearML.

    Args:
        monkeypatch: Fixture do pytest para monkey patching
        disponivel: Se ClearML deve estar disponível ou não
    """
    if disponivel:
        # Mock básico do ClearML
        class MockPipelineDecorator:
            @staticmethod
            def component(**kwargs):
                def decorator(func):
                    return func

                return decorator

        monkeypatch.setattr("funcoes.processamento._CLEARML_DISPONIVEL", True)
        monkeypatch.setattr(
            "funcoes.processamento.PipelineDecorator", MockPipelineDecorator
        )
    else:
        monkeypatch.setattr("funcoes.processamento._CLEARML_DISPONIVEL", False)


def assert_dataframe_estrutura_valida(df: pd.DataFrame, esperado_min_colunas: int = 3):
    """
    Utilitário para validar estrutura básica de DataFrames em testes.

    Args:
        df: DataFrame para validar
        esperado_min_colunas: Número mínimo esperado de colunas
    """
    assert isinstance(df, pd.DataFrame), "Resultado deve ser um DataFrame"
    assert len(df) > 0, "DataFrame não deve estar vazio"
    assert (
        len(df.columns) >= esperado_min_colunas
    ), f"DataFrame deve ter pelo menos {esperado_min_colunas} colunas"
    assert not df.isna().all().all(), "DataFrame não deve ser totalmente NaN"
