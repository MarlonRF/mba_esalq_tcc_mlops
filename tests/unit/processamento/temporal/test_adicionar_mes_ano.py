"""Testes para adicionar_mes_ano."""
import pytest
import pandas as pd
from src.processamento.temporal.adicionar_mes_ano import adicionar_mes_ano


def test_adicionar_mes_ano():
    """Testa se a função adiciona coluna mes-ano corretamente."""
    df = pd.DataFrame({
        'data': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-01-25'])
    })
    
    result = adicionar_mes_ano(df, 'data', 'mes-ano')
    
    assert 'mes-ano' in result.columns
    assert result['mes-ano'].tolist() == ['2023-01', '2023-02', '2023-01']
