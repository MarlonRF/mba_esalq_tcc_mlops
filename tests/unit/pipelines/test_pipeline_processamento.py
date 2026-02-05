"""
Testes unitários para o pipeline de processamento.
"""
import pandas as pd
import numpy as np
import pytest
from datetime import datetime

from src.pipelines.pipeline_processamento import executar_pipeline_processamento


@pytest.fixture
def df_basico():
    """DataFrame básico para testes."""
    return pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Hora': ['10:00:00', '11:00:00', '12:00:00'],
        'idade': [25, 30, 35],
        'peso': [70.5, 80.2, 75.8],
        'altura': [1.75, 1.80, 1.70],
        'sexo': ['m', 'f', 'm'],
        'temperatura': [25.5, 26.0, 24.8],
    })


@pytest.fixture
def df_com_faltantes():
    """DataFrame com valores faltantes para testar imputação."""
    return pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Hora': ['10:00:00', '11:00:00', '12:00:00', '13:00:00'],
        'idade': [25, np.nan, 35, 40],
        'peso': [70.5, 80.2, np.nan, 85.0],
        'altura': [1.75, 1.80, 1.70, np.nan],
        'sexo': ['m', 'f', None, 'f'],
        'temperatura': [25.5, np.nan, 24.8, 26.2],
    })


@pytest.fixture
def df_com_substituicoes():
    """DataFrame com valores que precisam substituição."""
    return pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Hora': ['10:00:00', '11:00:00', '12:00:00'],
        'idade': [25, 99, 35],  # 99 deve ser substituído por 0
        'peso': [70.5, 80.2, 75.8],
        'sexo': ['m', 'F', 'x'],  # 'F' -> 'f', 'x' -> 0
    })


def test_pipeline_processamento_basico(df_basico):
    """Testa execução básica do pipeline sem erros."""
    resultado = executar_pipeline_processamento(
        df_basico,
        criar_agrupamento_temporal=True
    )
    
    assert isinstance(resultado, pd.DataFrame)
    assert len(resultado) == len(df_basico)
    assert 'mes-ano' in resultado.columns  # Agrupamento temporal criado


def test_pipeline_padroniza_nomes_colunas(df_basico):
    """Testa se nomes de colunas são padronizados (lowercase, sem espaços)."""
    resultado = executar_pipeline_processamento(df_basico)
    
    # Todas as colunas devem estar em lowercase
    assert all(c.islower() for c in resultado.columns)
    # 'Data' vira 'data', 'Hora' vira 'hora'
    assert 'data' in resultado.columns
    assert 'hora' in resultado.columns


def test_pipeline_conversao_tipos():
    """Testa conversão correta de tipos de dados."""
    df = pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02'],
        'Hora': ['10:00:00', '11:00:00'],
        'idade': ['25', '30'],
        'peso': ['70.5', '80.2'],
        'sexo': ['m', 'f'],
    })
    
    resultado = executar_pipeline_processamento(df)
    
    # Verificar tipos após conversão
    assert pd.api.types.is_datetime64_any_dtype(resultado['data'])
    assert pd.api.types.is_datetime64_any_dtype(resultado['hora'])
    assert pd.api.types.is_integer_dtype(resultado['idade'])
    assert pd.api.types.is_float_dtype(resultado['peso'])
    assert pd.api.types.is_string_dtype(resultado['sexo'])


def test_pipeline_substituicoes(df_com_substituicoes):
    """Testa se substituições de limpeza são aplicadas."""
    substituicoes = {
        99: 0,
        'x': 0,
        'F': 'f'
    }
    
    resultado = executar_pipeline_processamento(
        df_com_substituicoes,
        substituicoes=substituicoes
    )
    
    # Verificar substituições
    assert 99 not in resultado['idade'].values
    assert 'x' not in resultado['sexo'].values
    assert 'F' not in resultado['sexo'].values


def test_pipeline_imputacao_numerica(df_com_faltantes):
    """Testa imputação de valores numéricos faltantes."""
    resultado = executar_pipeline_processamento(
        df_com_faltantes,
        metodo_imputacao_numerica='median'
    )
    
    # Não deve haver valores faltantes em colunas numéricas
    assert resultado['idade'].isna().sum() == 0
    assert resultado['peso'].isna().sum() == 0
    assert resultado['altura'].isna().sum() == 0


def test_pipeline_imputacao_categorica(df_com_faltantes):
    """Testa imputação de valores categóricos faltantes."""
    resultado = executar_pipeline_processamento(
        df_com_faltantes,
        metodo_imputacao_categorica='mode'
    )
    
    # Não deve haver valores faltantes em colunas categóricas
    assert resultado['sexo'].isna().sum() == 0


def test_pipeline_imputacao_customizada():
    """Testa imputação customizada por coluna."""
    df = pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Hora': ['10:00:00', '11:00:00', '12:00:00', '13:00:00'],
        'idade': [25, np.nan, 35, 40],
        'peso': [70.5, 80.2, np.nan, 85.0],
        'altura': [1.75, 1.80, 1.70, np.nan],
    })
    
    config_imputacao = {
        'idade': 'median',
        'peso': 'mean',
        'altura': 1.75  # Valor constante
    }
    
    resultado = executar_pipeline_processamento(
        df,
        config_imputacao_customizada=config_imputacao
    )
    
    # Verificar que não há valores faltantes
    assert resultado['idade'].isna().sum() == 0
    assert resultado['peso'].isna().sum() == 0
    assert resultado['altura'].isna().sum() == 0
    
    # Verificar que altura foi imputada com 1.75
    assert resultado.loc[3, 'altura'] == 1.75


def test_pipeline_agrupamento_temporal(df_basico):
    """Testa criação de coluna de agrupamento temporal."""
    resultado = executar_pipeline_processamento(
        df_basico,
        criar_agrupamento_temporal=True,
        nome_coluna_agrupamento='mes-ano'
    )
    
    assert 'mes-ano' in resultado.columns
    # Todas as linhas devem ter valor de agrupamento
    assert resultado['mes-ano'].isna().sum() == 0


def test_pipeline_sem_agrupamento_temporal(df_basico):
    """Testa que agrupamento temporal não é criado quando desabilitado."""
    resultado = executar_pipeline_processamento(
        df_basico,
        criar_agrupamento_temporal=False
    )
    
    assert 'mes-ano' not in resultado.columns


def test_pipeline_nao_modifica_original(df_basico):
    """Testa que DataFrame original não é modificado."""
    df_original = df_basico.copy()
    
    executar_pipeline_processamento(df_basico)
    
    # DataFrame original deve permanecer inalterado
    pd.testing.assert_frame_equal(df_basico, df_original)


def test_pipeline_shape_preservado(df_basico):
    """Testa que número de linhas é preservado."""
    resultado = executar_pipeline_processamento(df_basico)
    
    assert len(resultado) == len(df_basico)


def test_pipeline_com_dataframe_vazio():
    """Testa comportamento com DataFrame vazio."""
    df_vazio = pd.DataFrame()
    
    # Deve executar sem erros
    resultado = executar_pipeline_processamento(df_vazio)
    
    assert isinstance(resultado, pd.DataFrame)
    assert len(resultado) == 0


def test_pipeline_parametros_defaults():
    """Testa que pipeline funciona com configurações padrão do config."""
    df = pd.DataFrame({
        'Data': ['2023-01-01', '2023-01-02'],
        'Hora': ['10:00:00', '11:00:00'],
        'idade': [25, 30],
        'peso': [70.5, 80.2],
        'sexo': ['m', 'f'],
    })
    
    # Deve usar configurações do config.py automaticamente
    resultado = executar_pipeline_processamento(df)
    
    assert isinstance(resultado, pd.DataFrame)
    assert len(resultado) == len(df)
