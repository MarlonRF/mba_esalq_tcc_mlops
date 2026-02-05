"""
Testes unitários para função aplicar_substituicoes.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestAplicarSubstituicoes:
    """Testes para função aplicar_substituicoes"""

    def test_substituicoes_basicas(self):
        """Testa substituições básicas de valores"""
        from src.processamento.limpeza.aplicar_substituicoes import aplicar_substituicoes
        
        df = pd.DataFrame({
            "status": ["ativo", "inativo", "ativo"],
            "tipo": ["A", "B", "A"]
        })
        
        substituicoes = {
            "status": {"ativo": "ATIVO", "inativo": "INATIVO"}
        }
        
        df_resultado = aplicar_substituicoes(df, substituicoes)
        
        assert df_resultado["status"].iloc[0] == "ATIVO"
        assert df_resultado["status"].iloc[1] == "INATIVO"
        
    def test_coluna_nao_afetada(self):
        """Testa que colunas não especificadas não são alteradas"""
        from src.processamento.limpeza.aplicar_substituicoes import aplicar_substituicoes
        
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        substituicoes = {"A": {1: 10}}
        
        df_resultado = aplicar_substituicoes(df, substituicoes)
        
        assert df_resultado["A"].iloc[0] == 10
        assert df_resultado["B"].iloc[0] == 3  # Não alterado
        
    def test_dicionario_vazio(self):
        """Testa que dicionário vazio não altera DataFrame"""
        from src.processamento.limpeza.aplicar_substituicoes import aplicar_substituicoes
        
        df = pd.DataFrame({"A": [1, 2]})
        df_resultado = aplicar_substituicoes(df, {})
        
        pd.testing.assert_frame_equal(df, df_resultado)
