"""Teste de integracao do pipeline de processamento com configuracao generica."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# NOTA: Estes testes usam funções antigas da pasta 'legacy' que foram descontinuadas.
# Os testes foram desabilitados. Use test_pipeline_end_to_end.py e test_cenarios_reais.py
# para testes de integração atualizados.

pytest.skip("Testes antigos usando módulos legacy descontinuados", allow_module_level=True)


@pytest.mark.integration
def test_processar_dados_com_config_generica():
    dados_brutos = pd.DataFrame(
        {
            "Data": ["15/01/2025", "16/01/2025", "17/01/2025"],
            "Hora": ["09:00", "10:30", "11:45"],
            "TARGET_RAW": [1, 2, 3],
            "Q1": ["x", 2, np.nan],
            "Q2": [1, np.nan, 3],
            "Category": [None, "A", "B"],
            "tmedia": [25.0, 26.0, 27.0],
            "ur": [60.0, 65.0, 70.0],
            "tu": [np.nan, 24.0, np.nan],
            "rad_total": [np.nan, 100.0, 120.0],
            "rad_avg": [5.0, np.nan, 10.0],
        }
    )

    cfg = PipelineConfig(
        type_dict={
            "data": "datetime64[ns]",
            "hora": "datetime64[ns]",
            "target_raw": "Int64",
            "q1": "Int64",
            "q2": "Int64",
            "category": "string",
            "tmedia": "float64",
            "ur": "float64",
            "tu": "float64",
            "rad_total": "float64",
            "rad_avg": "float64",
        },
        substituicoes_globais={"x": np.nan, 99: np.nan},
        substituicoes_perguntas={"x": np.nan, "99": np.nan},
        colunas_perguntas=["q1", "q2"],
        colunas_backfill=["q1", "category"],
        coluna_radiacao_total="rad_total",
        coluna_radiacao_media="rad_avg",
        janela_media_rolante=2,
        coluna_alvo_origem="target_raw",
        coluna_alvo_destino="target",
        mapa_alvo={1: "low", 2: "mid", 3: "high"},
        renomear_colunas={
            "data": "dt",
            "hora": "hr",
            "target_raw": "target_raw",
            "target": "target",
            "q1": "q1_resp",
            "q2": "q2_resp",
            "category": "category",
            "rad_total": "rad_total_filled",
            "rad_avg": "rad_avg_filled",
            "tu": "tu_filled",
            "mes-ano": "mes_ano",
            "data_cplt": "data_completa",
        },
        substituir_renomear=True,
    )

    resultado = processar_dados(dados_brutos, cfg)

    # Colunas essenciais renomeadas e preservadas
    colunas_esperadas = {
        "dt",
        "hr",
        "mes_ano",
        "data_completa",
        "target",
        "q1_resp",
        "q2_resp",
        "rad_total_filled",
        "rad_avg_filled",
        "tu_filled",
    }
    assert colunas_esperadas.issubset(set(resultado.columns))

    # Tipos aplicados
    assert pd.api.types.is_datetime64_any_dtype(resultado["dt"])
    assert pd.api.types.is_datetime64_any_dtype(resultado["hr"]) or resultado["hr"].dtype == "object"
    assert all(isinstance(v, str) or pd.isna(v) for v in resultado["category"])
    numeros_q1 = pd.to_numeric(resultado["q1_resp"], errors="coerce")
    assert numeros_q1.isna().sum() == 1

    # Data/hora combinadas e agrupamento temporal criado
    assert isinstance(resultado.loc[0, "data_completa"], pd.Timestamp)
    assert resultado.loc[0, "data_completa"].hour == 9
    assert resultado.loc[0, "mes_ano"] == "01 - 2025"

    # Imputacoes e backfill
    assert pd.isna(resultado.loc[0, "q1_resp"]) is False  # primeira linha preenchida via bfill
    assert pd.isna(resultado.loc[1, "q1_resp"]) is False
    assert pd.isna(resultado.loc[2, "q1_resp"]) is True
    assert not resultado["tu_filled"].isna().any()  # TU calculado quando faltante
    assert resultado["rad_total_filled"].isna().sum() <= 1  # primeira linha pode seguir NaN se janela nao cobre
    assert not resultado["rad_avg_filled"].isna().any()

    # Mapeamento de alvo
    assert resultado["target"].tolist() == ["low", "mid", "high"]

    # Nenhuma coluna inesperada foi descartada
    assert "category" in resultado.columns