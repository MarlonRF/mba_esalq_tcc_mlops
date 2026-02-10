"""Utilitarios de configuracao para execucao da API."""

import os
from dataclasses import dataclass
from pathlib import Path


def remover_sufixo_pkl(caminho_modelo: str) -> str:
    if caminho_modelo.endswith(".pkl"):
        return caminho_modelo[:-4]
    return caminho_modelo


def resolver_nome_modelo() -> str:
    valor_ambiente = os.environ.get("API_CAMINHO_MODELO") or os.environ.get("API_MODEL_PATH")
    if valor_ambiente:
        return remover_sufixo_pkl(valor_ambiente)

    candidatos = [
        Path("api"),  # execucao na raiz do repositorio (espera api.pkl)
        Path(__file__).resolve().parent / "api",  # execucao dentro de src/api
        Path("/app/api"),  # diretorio padrao no container
    ]

    for candidato in candidatos:
        if candidato.with_suffix(".pkl").exists():
            return str(candidato)

    return "api"


@dataclass(frozen=True)
class ConfiguracoesApi:
    endereco_host: str
    porta: int
    nome_modelo: str


def obter_configuracoes_api() -> ConfiguracoesApi:
    return ConfiguracoesApi(
        endereco_host=os.environ.get("API_ENDERECO_HOST", os.environ.get("API_HOST", "0.0.0.0")),
        porta=int(os.environ.get("API_PORTA", os.environ.get("PORT", os.environ.get("API_PORT", "8080")))),
        nome_modelo=resolver_nome_modelo(),
    )
