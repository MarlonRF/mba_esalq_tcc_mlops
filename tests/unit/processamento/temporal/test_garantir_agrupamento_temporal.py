"""
Testes unitários para função garantir_agrupamento_temporal.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestGarantirAgrupamentoTemporal:
    """Testes para função garantir_agrupamento_temporal"""

    def test_cria_coluna_mes_ano(self):
        """Testa criação da coluna mes-ano"""
        from src.processamento.temporal.garantir_agrupamento_temporal import garantir_agrupamento_temporal
        
        df = pd.DataFrame({
            "data": ["2025-01-15", "2025-02-20"],
            "hora": ["09:00", "14:00"],
            "valor": [100, 200]
        })
        
        df_resultado = garantir_agrupamento_temporal(df, "data", "hora")
        
        assert "mes-ano" in df_resultado.columns
        
    def test_preserva_coluna_existente(self):
        """Testa que coluna existente não é sobrescrita"""
        from src.processamento.temporal.garantir_agrupamento_temporal import garantir_agrupamento_temporal
        
        df = pd.DataFrame({
            "data": ["2025-01-15"],
            "hora": ["09:00"],
            "mes-ano": ["ORIGINAL"]
        })
        
        df_resultado = garantir_agrupamento_temporal(df, "data", "hora")
        
        assert df_resultado["mes-ano"].iloc[0] == "ORIGINAL"
