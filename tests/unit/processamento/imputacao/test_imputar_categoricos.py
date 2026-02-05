"""
Testes unitários para função imputar_categoricos.
"""
import pandas as pd
import pytest
import numpy as np


@pytest.mark.unit
class TestImputarCategoricos:
    """Testes para função imputar_categoricos"""

    def test_imputacao_moda(self):
        """Testa imputação com moda (valor mais frequente)"""
        from src.processamento.imputacao.imputar_categoricos import imputar_categoricos
        
        df = pd.DataFrame({"cor": ["vermelho", "azul", "vermelho", np.nan]})
        df_resultado = imputar_categoricos(df, metodo="most_frequent")
        
        # "vermelho" é a moda
        assert df_resultado["cor"].notna().all()
        assert df_resultado["cor"].iloc[3] == "vermelho"
        
    def test_imputacao_constante(self):
        """Testa imputação com valor constante"""
        from src.processamento.imputacao.imputar_categoricos import imputar_categoricos
        
        df = pd.DataFrame({"categoria": ["A", "B", np.nan]})
        df_resultado = imputar_categoricos(df, metodo="constant", valor_constante="DESCONHECIDO")
        
        assert df_resultado["categoria"].iloc[2] == "DESCONHECIDO"
        
    def test_preserva_nao_categoricos(self):
        """Testa que colunas não categóricas não são alteradas"""
        from src.processamento.imputacao.imputar_categoricos import imputar_categoricos
        
        df = pd.DataFrame({
            "texto": ["A", "B", np.nan],
            "numero": [1, 2, 3]
        })
        
        df_resultado = imputar_categoricos(df, metodo="most_frequent")
        
        # Coluna numérica não deve ser alterada
        assert df_resultado["numero"].iloc[2] == 3
