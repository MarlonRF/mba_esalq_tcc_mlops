"""
Testes unitários para função converter_colunas_float.
"""
import pandas as pd
import pytest
import numpy as np


@pytest.mark.unit
class TestConverterColunasFloat:
    """Testes para função converter_colunas_float"""

    def test_conversao_basica(self):
        """Testa conversão básica de strings para float"""
        from src.processamento.limpeza.converter_colunas_float import converter_colunas_float
        
        df = pd.DataFrame({"valor": ["1.5", "2.3", "10.0"]})
        df_resultado = converter_colunas_float(df, ["valor"])
        
        assert df_resultado["valor"].dtype == float
        assert df_resultado["valor"].iloc[0] == 1.5
        
    def test_conversao_virgula_decimal(self):
        """Testa conversão de números com vírgula decimal brasileira"""
        from src.processamento.limpeza.converter_colunas_float import converter_colunas_float
        
        df = pd.DataFrame({"preco": ["1,5", "2,3", "10,7"]})
        df_resultado = converter_colunas_float(df, ["preco"])
        
        assert df_resultado["preco"].iloc[0] == 1.5
        assert df_resultado["preco"].iloc[1] == 2.3
        
    def test_valores_invalidos_tornam_nan(self):
        """Testa que valores inválidos se tornam NaN"""
        from src.processamento.limpeza.converter_colunas_float import converter_colunas_float
        
        df = pd.DataFrame({"num": ["1.5", "abc", "2.3"]})
        df_resultado = converter_colunas_float(df, ["num"])
        
        assert df_resultado["num"].iloc[0] == 1.5
        assert np.isnan(df_resultado["num"].iloc[1])
        assert df_resultado["num"].iloc[2] == 2.3
        
    def test_colunas_inexistentes_ignoradas(self):
        """Testa que colunas inexistentes são ignoradas"""
        from src.processamento.limpeza.converter_colunas_float import converter_colunas_float
        
        df = pd.DataFrame({"A": ["1.5"]})
        df_resultado = converter_colunas_float(df, ["A", "B", "C"])
        
        assert "A" in df_resultado.columns
        assert df_resultado["A"].iloc[0] == 1.5
