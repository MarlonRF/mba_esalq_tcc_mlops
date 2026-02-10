"""Testes do contrato de saida da aplicacao em modo legado e modo novo."""

from fastapi.testclient import TestClient

from src.api.aplicacao import criar_aplicacao


class PreditorFalso:
    """Preditor simples para testes de contrato sem modelo real."""

    def prever_rotulo(self, dados):
        return "Confortavel"


def corpo_entrada_valido():
    return {
        "idade_anos": 30,
        "peso_kg": 70.0,
        "altura_cm": 175,
        "sexo_biologico": "m",
        "temperatura_media_c": 25.0,
        "umidade_relativa_percent": 60.0,
        "radiacao_solar_media_wm2": 400.0,
    }


def test_contrato_com_legado_ativo(monkeypatch):
    """Com legado ativo, resposta traz campos novo e antigo."""
    monkeypatch.setenv("API_COMPAT_LEGADO_ATIVA", "1")
    monkeypatch.setenv("API_DATA_LIMITE_LEGADO", "2026-06-30")

    cliente = TestClient(criar_aplicacao(PreditorFalso()))

    resposta_raiz = cliente.get("/")
    dados_raiz = resposta_raiz.json()

    assert resposta_raiz.status_code == 200
    assert dados_raiz["mensagem"] == "API de Conforto Termico em execucao!"
    assert dados_raiz["message"] == dados_raiz["mensagem"]
    assert resposta_raiz.headers["X-Compatibilidade-Legado"] == "ativa"
    assert resposta_raiz.headers["X-Data-Limite-Legado"] == "2026-06-30"

    resposta_predicao = cliente.post("/predict", json=corpo_entrada_valido())
    dados_predicao = resposta_predicao.json()

    assert resposta_predicao.status_code == 200
    assert dados_predicao["predicao"] == "Confortavel"
    assert dados_predicao["prediction"] == dados_predicao["predicao"]
    assert resposta_predicao.headers["X-Compatibilidade-Legado"] == "ativa"


def test_contrato_com_legado_inativo(monkeypatch):
    """Com legado inativo, resposta traz apenas campos oficiais."""
    monkeypatch.setenv("API_COMPAT_LEGADO_ATIVA", "0")
    monkeypatch.setenv("API_DATA_LIMITE_LEGADO", "2026-06-30")

    cliente = TestClient(criar_aplicacao(PreditorFalso()))

    resposta_raiz = cliente.get("/")
    dados_raiz = resposta_raiz.json()

    assert resposta_raiz.status_code == 200
    assert dados_raiz["mensagem"] == "API de Conforto Termico em execucao!"
    assert "message" not in dados_raiz
    assert resposta_raiz.headers["X-Compatibilidade-Legado"] == "inativa"

    resposta_predicao = cliente.post("/predict", json=corpo_entrada_valido())
    dados_predicao = resposta_predicao.json()

    assert resposta_predicao.status_code == 200
    assert dados_predicao["predicao"] == "Confortavel"
    assert "prediction" not in dados_predicao
    assert resposta_predicao.headers["X-Compatibilidade-Legado"] == "inativa"

