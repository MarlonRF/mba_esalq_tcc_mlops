"""
Testes unitários para função adicionar_features_derivadas.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestAdicionarFeaturesDerivadas:
    """Testes para função adicionar_features_derivadas"""

    def test_adicionar_imc(self):
        """Testa adição de feature IMC"""
        from src.processamento.derivadas.adicionar_features_derivadas import adicionar_features_derivadas
        
        df = pd.DataFrame({
            "peso": [70, 80],
            "altura": [175, 180]
        })
        
        df_resultado = adicionar_features_derivadas(df, ["imc"])
        
        assert "IMC" in df_resultado.columns
        assert df_resultado["IMC"].notna().all()
        
    def test_adicionar_heat_index(self):
        """Testa adição de heat index"""
        from src.processamento.derivadas.adicionar_features_derivadas import adicionar_features_derivadas
        
        df = pd.DataFrame({
            "tmedia": [25, 30],
            "ur": [60, 70]
        })
        
        df_resultado = adicionar_features_derivadas(df, ["heat_index"])
        
        assert "heat_index" in df_resultado.columns
        
    def test_multiplas_features(self):
        """Testa adição de múltiplas features"""
        from src.processamento.derivadas.adicionar_features_derivadas import adicionar_features_derivadas
        
        df = pd.DataFrame({
            "peso": [70],
            "altura": [175],
            "tmedia": [25],
            "ur": [60]
        })
        
        df_resultado = adicionar_features_derivadas(
            df, ["imc", "heat_index", "dew_point", "t*u"]
        )
        
        assert "IMC" in df_resultado.columns
        assert "heat_index" in df_resultado.columns
        assert "dew_point" in df_resultado.columns
        assert "t_u" in df_resultado.columns
        
    def test_lista_vazia(self):
        """Testa que lista vazia não modifica DataFrame"""
        from src.processamento.derivadas.adicionar_features_derivadas import adicionar_features_derivadas
        
        df = pd.DataFrame({"A": [1, 2]})
        df_resultado = adicionar_features_derivadas(df, [])
        
        pd.testing.assert_frame_equal(df, df_resultado)
