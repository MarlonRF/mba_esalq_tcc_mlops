"""Testes unitarios para configuracoes da API."""

from src.api.configuracoes import (
    obter_configuracoes_api,
    remover_sufixo_pkl,
    resolver_nome_modelo,
)


def test_remover_sufixo_pkl_remove_extensao():
    """Remove apenas o sufixo .pkl quando presente."""
    assert remover_sufixo_pkl("modelo_final.pkl") == "modelo_final"
    assert remover_sufixo_pkl("modelo_final") == "modelo_final"


def test_resolver_nome_modelo_prioriza_variavel_portuguesa(monkeypatch):
    """A variavel nova deve ter prioridade sobre a variavel legado."""
    monkeypatch.setenv("API_CAMINHO_MODELO", "modelos/modelo_pt.pkl")
    monkeypatch.setenv("API_MODEL_PATH", "modelos/modelo_legado.pkl")
    assert resolver_nome_modelo() == "modelos/modelo_pt"


def test_resolver_nome_modelo_usa_variavel_legado_se_preciso(monkeypatch):
    """Mantem compatibilidade com API_MODEL_PATH."""
    monkeypatch.delenv("API_CAMINHO_MODELO", raising=False)
    monkeypatch.setenv("API_MODEL_PATH", "modelos/modelo_legado.pkl")
    assert resolver_nome_modelo() == "modelos/modelo_legado"


def test_obter_configuracoes_api_ler_variaveis_portuguesas(monkeypatch):
    """Le parametros principais da API pelas variaveis em portugues."""
    monkeypatch.setenv("API_ENDERECO_HOST", "127.0.0.1")
    monkeypatch.setenv("API_PORTA", "9001")
    monkeypatch.setenv("API_CAMINHO_MODELO", "artefatos/modelo_api.pkl")

    configuracoes = obter_configuracoes_api()

    assert configuracoes.endereco_host == "127.0.0.1"
    assert configuracoes.porta == 9001
    assert configuracoes.nome_modelo == "artefatos/modelo_api"

