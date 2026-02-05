"""
Testes unitários para função codificar_label.
"""
import pandas as pd
import pytest


@pytest.mark.unit
class TestCodificarLabel:
    """Testes para função codificar_label"""

    def test_codificacao_basica(self):
        """Testa codificação básica de categorias"""
        from src.processamento.codificacao.codificar_label import codificar_label
        
        serie = pd.Series(["maçã", "banana", "maçã", "laranja"])
        codigos, mapeamento = codificar_label(serie)
        
        # Verifica que retornou Series e dict
        assert isinstance(codigos, pd.Series)
        assert isinstance(mapeamento, dict)
        
        # Verifica que categorias iguais têm o mesmo código
        assert codigos.iloc[0] == codigos.iloc[2]
        
        # Verifica que todas as categorias foram mapeadas
        assert len(mapeamento) == 3  # maçã, banana, laranja
        
    def test_valores_faltantes(self):
        """Testa tratamento de valores faltantes"""
        from src.processamento.codificacao.codificar_label import codificar_label
        
        serie = pd.Series(["maçã", None, "banana", pd.NA])
        codigos, mapeamento = codificar_label(serie)
        
        # Valores faltantes devem ser tratados
        assert codigos.notna().all()
        assert "__faltante__" in mapeamento.values()
        
    def test_mapeamento_reverso(self):
        """Testa se o mapeamento permite recuperar categorias originais"""
        from src.processamento.codificacao.codificar_label import codificar_label
        
        serie = pd.Series(["A", "B", "C", "A"])
        codigos, mapeamento = codificar_label(serie)
        
        # Verifica se podemos reverter o código para categoria
        for codigo, categoria_original in zip(codigos, serie):
            assert mapeamento[int(codigo)] == str(categoria_original)
