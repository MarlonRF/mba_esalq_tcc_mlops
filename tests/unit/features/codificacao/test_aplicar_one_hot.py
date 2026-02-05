"""
Testes unitários para função aplicar_one_hot.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestAplicarOneHot:
    """Testes para função aplicar_one_hot"""

    def test_one_hot_basico(self):
        """Testa one-hot encoding básico"""
        from src.processamento.codificacao.aplicar_one_hot import aplicar_one_hot
        
        df = pd.DataFrame({"cor": ["vermelho", "azul", "verde", "vermelho"]})
        df_resultado = aplicar_one_hot(df, ["cor"])
        
        # Verifica que colunas one-hot foram criadas
        assert "cor_vermelho" in df_resultado.columns or "cor_azul" in df_resultado.columns
        
        # Verifica valores binários
        colunas_onehot = [col for col in df_resultado.columns if col.startswith("cor_")]
        for col in colunas_onehot:
            assert df_resultado[col].isin([0, 1]).all()
            
    def test_drop_first(self):
        """Testa parâmetro drop_first para evitar colinearidade"""
        from src.processamento.codificacao.aplicar_one_hot import aplicar_one_hot
        
        df = pd.DataFrame({"cat": ["A", "B", "C"]})
        
        df_sem_drop = aplicar_one_hot(df, ["cat"], drop_first=False)
        df_com_drop = aplicar_one_hot(df, ["cat"], drop_first=True)
        
        colunas_sem_drop = [c for c in df_sem_drop.columns if c.startswith("cat_")]
        colunas_com_drop = [c for c in df_com_drop.columns if c.startswith("cat_")]
        
        assert len(colunas_com_drop) == len(colunas_sem_drop) - 1
        
    def test_colunas_vazias(self):
        """Testa comportamento com lista vazia de colunas"""
        from src.processamento.codificacao.aplicar_one_hot import aplicar_one_hot
        
        df = pd.DataFrame({"A": [1, 2]})
        df_resultado = aplicar_one_hot(df, [])
        
        pd.testing.assert_frame_equal(df, df_resultado)
