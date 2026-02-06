"""
Testes unitários para função aplicar_codificacao_label.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestAplicarCodificacaoLabel:
    """Testes para função aplicar_codificacao_label"""

    def test_codificacao_multiplas_colunas(self):
        """Testa codificação de múltiplas colunas"""
        from src.features.codificacao.aplicar_codificacao_rotulos import aplicar_codificacao_rotulos
        
        df = pd.DataFrame({
            "fruta": ["maçã", "banana", "maçã"],
            "cor": ["vermelha", "amarela", "verde"]
        })
        
        df_resultado, artefatos = aplicar_codificacao_rotulos(df, ["fruta", "cor"])
        
        # Verifica que novas colunas foram criadas
        assert "fruta_cod" in df_resultado.columns
        assert "cor_cod" in df_resultado.columns
        
        # Verifica que artefatos contêm mapeamentos
        assert "fruta" in artefatos
        assert "cor" in artefatos
        assert isinstance(artefatos["fruta"], dict)
        
    def test_colunas_inexistentes_ignoradas(self):
        """Testa que colunas inexistentes são ignoradas"""
        from src.features.codificacao.aplicar_codificacao_rotulos import aplicar_codificacao_rotulos
        
        df = pd.DataFrame({"A": ["x", "y"]})
        df_resultado, artefatos = aplicar_codificacao_rotulos(df, ["A", "B", "C"])
        
        # Apenas coluna A deve ser codificada
        assert "A_cod" in df_resultado.columns
        assert "B_cod" not in df_resultado.columns
        assert len(artefatos) == 1
        
    def test_sufixo_personalizado(self):
        """Testa uso de sufixo personalizado"""
        from src.features.codificacao.aplicar_codificacao_rotulos import aplicar_codificacao_rotulos
        
        df = pd.DataFrame({"categoria": ["A", "B"]})
        df_resultado, _ = aplicar_codificacao_rotulos(df, ["categoria"], sufixo="_encoded")
        
        assert "categoria_encoded" in df_resultado.columns
        
    def test_dataframe_original_nao_modificado(self):
        """Testa que DataFrame original não é modificado"""
        from src.features.codificacao.aplicar_codificacao_rotulos import aplicar_codificacao_rotulos
        
        df = pd.DataFrame({"col": ["A", "B"]})
        df_original = df.copy()
        
        aplicar_codificacao_rotulos(df, ["col"])
        
        pd.testing.assert_frame_equal(df, df_original)
