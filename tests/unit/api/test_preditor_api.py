"""Testes unitarios para o preditor da API."""

import sys
import types

import pandas as pd

from src.api.preditor import PreditorPyCaret


def registrar_pycaret_falso(monkeypatch, rotulo_saida):
    """Registra modulo pycaret falso para testar sem carregar modelo real."""
    chamadas = {"carregamentos": 0, "predicoes": 0, "nome_modelo": None}

    modulo_pycaret = types.ModuleType("pycaret")
    modulo_classificacao = types.ModuleType("pycaret.classification")

    def carregar_modelo(nome_modelo):
        chamadas["carregamentos"] += 1
        chamadas["nome_modelo"] = nome_modelo
        return {"nome_modelo": nome_modelo}

    def predizer_modelo(modelo, data):
        chamadas["predicoes"] += 1
        return pd.DataFrame({"prediction_label": [rotulo_saida]})

    modulo_classificacao.load_model = carregar_modelo
    modulo_classificacao.predict_model = predizer_modelo
    modulo_pycaret.classification = modulo_classificacao

    monkeypatch.setitem(sys.modules, "pycaret", modulo_pycaret)
    monkeypatch.setitem(sys.modules, "pycaret.classification", modulo_classificacao)

    return chamadas


def test_preditor_pycaret_retorna_rotulo(monkeypatch):
    """Retorna rotulo previsto como string."""
    chamadas = registrar_pycaret_falso(monkeypatch, "Confortavel")
    preditor = PreditorPyCaret("modelo_teste")

    rotulo = preditor.prever_rotulo(pd.DataFrame([{"x": 1}]))

    assert rotulo == "Confortavel"
    assert chamadas["carregamentos"] == 1
    assert chamadas["predicoes"] == 1
    assert chamadas["nome_modelo"] == "modelo_teste"


def test_preditor_pycaret_carrega_modelo_apenas_uma_vez(monkeypatch):
    """Evita recarregar modelo ao chamar predicao multiplas vezes."""
    chamadas = registrar_pycaret_falso(monkeypatch, "Neutro")
    preditor = PreditorPyCaret("modelo_unico")

    preditor.prever_rotulo(pd.DataFrame([{"x": 1}]))
    preditor.prever_rotulo(pd.DataFrame([{"x": 2}]))

    assert chamadas["carregamentos"] == 1
    assert chamadas["predicoes"] == 2


def test_preditor_pycaret_converte_rotulo_para_string(monkeypatch):
    """Converte resposta para string quando necessario."""
    registrar_pycaret_falso(monkeypatch, 123)
    preditor = PreditorPyCaret("modelo_numerico")

    rotulo = preditor.prever_rotulo(pd.DataFrame([{"x": 1}]))

    assert rotulo == "123"

