"""
Testes unitários para io_local.py
"""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from src.utils.io.io_local import load_dataframe, _read_csv_robust


@pytest.fixture
def csv_file():
    """Cria arquivo CSV temporário para testes."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('col1,col2,col3\n')
        f.write('1,2,3\n')
        f.write('4,5,6\n')
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def excel_file():
    """Cria arquivo Excel temporário para testes."""
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        temp_path = f.name
    df.to_excel(temp_path, index=False)
    yield temp_path
    os.unlink(temp_path)


def test_load_dataframe_csv(csv_file):
    """Testa carregamento de arquivo CSV."""
    df = load_dataframe(csv_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'col1' in df.columns


def test_load_dataframe_excel(excel_file):
    """Testa carregamento de arquivo Excel."""
    df = load_dataframe(excel_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'A' in df.columns


def test_load_dataframe_arquivo_inexistente():
    """Testa erro ao carregar arquivo inexistente."""
    with pytest.raises(FileNotFoundError):
        load_dataframe('arquivo_inexistente.csv')


def test_read_csv_robust_comma_delimiter(csv_file):
    """Testa leitura robusta de CSV com vírgula."""
    df = _read_csv_robust(csv_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_read_csv_robust_semicolon_delimiter():
    """Testa detecção automática de delimitador ponto-e-vírgula."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('col1;col2;col3\n')
        f.write('1;2;3\n')
        temp_path = f.name
    
    try:
        df = _read_csv_robust(temp_path)
        assert len(df.columns) == 3
    finally:
        os.unlink(temp_path)


def test_load_dataframe_parquet():
    """Testa carregamento de arquivo Parquet."""
    df_original = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        temp_path = f.name
    
    try:
        df_original.to_parquet(temp_path)
        df_loaded = load_dataframe(temp_path)
        
        assert isinstance(df_loaded, pd.DataFrame)
        pd.testing.assert_frame_equal(df_loaded, df_original)
    finally:
        os.unlink(temp_path)
