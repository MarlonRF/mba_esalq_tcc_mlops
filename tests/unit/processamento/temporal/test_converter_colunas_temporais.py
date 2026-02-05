"""
Testes unitários para função converter_colunas_temporais.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestConverterColunasTemporais:
    """Testes para função converter_colunas_temporais"""

    def test_conversao_data_hora(self):
        """Testa conversão de colunas de data e hora"""
        from src.processamento.temporal.converter_colunas_temporais import converter_colunas_temporais
        
        df = pd.DataFrame({
            "data": ["2025-01-15", "2025-01-16"],
            "hora": ["09:00", "14:00"]
        })
        
        df_resultado = converter_colunas_temporais(df, "data", "hora")
        
        # Verifica que colunas foram convertidas
        assert pd.api.types.is_datetime64_any_dtype(df_resultado["data"])
        
    def test_formato_brasileiro(self):
        """Testa conversão com formato brasileiro (dd/mm/yyyy)"""
        from src.processamento.temporal.converter_colunas_temporais import converter_colunas_temporais
        
        df = pd.DataFrame({
            "data": ["15/01/2025", "16/01/2025"],
            "hora": ["09:00", "14:00"]
        })
        
        df_resultado = converter_colunas_temporais(df, "data", "hora")
        
        assert pd.api.types.is_datetime64_any_dtype(df_resultado["data"])
        
    def test_coluna_inexistente(self):
        """Testa comportamento com coluna inexistente"""
        from src.processamento.temporal.converter_colunas_temporais import converter_colunas_temporais
        
        df = pd.DataFrame({"A": [1, 2]})
        df_resultado = converter_colunas_temporais(df, "data_inexistente", "hora_inexistente")
        
        # Deve retornar DataFrame sem erro
        assert isinstance(df_resultado, pd.DataFrame)
