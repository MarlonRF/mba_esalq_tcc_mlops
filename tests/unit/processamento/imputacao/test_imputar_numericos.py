"""
Testes unitários para função imputar_numericos.
"""
import pandas as pd
import pytest
import numpy as np


@pytest.mark.unit
class TestImputarNumericos:
    """Testes para função imputar_numericos"""

    def test_imputacao_media(self):
        """Testa imputação com média"""
        from src.processamento.imputacao.imputar_numericos import imputar_numericos
        
        df = pd.DataFrame({"valores": [1.0, 2.0, np.nan, 4.0]})
        df_resultado = imputar_numericos(df, metodo="mean")
        
        # Média = (1+2+4)/3 = 2.33
        assert df_resultado["valores"].notna().all()
        assert pytest.approx(df_resultado["valores"].iloc[2], rel=0.1) == 2.33
        
    def test_imputacao_mediana(self):
        """Testa imputação com mediana"""
        from src.processamento.imputacao.imputar_numericos import imputar_numericos
        
        df = pd.DataFrame({"valores": [1.0, 2.0, np.nan, 4.0, 100.0]})
        df_resultado = imputar_numericos(df, metodo="median")
        
        # Mediana é mais robusta a outliers
        assert df_resultado["valores"].notna().all()
        
    def test_sem_valores_faltantes(self):
        """Testa que DataFrame sem NaN não é alterado"""
        from src.processamento.imputacao.imputar_numericos import imputar_numericos
        
        df = pd.DataFrame({"A": [1, 2, 3]})
        df_original = df.copy()
        
        df_resultado = imputar_numericos(df, metodo="mean")
        
        pd.testing.assert_frame_equal(df_resultado, df_original)
