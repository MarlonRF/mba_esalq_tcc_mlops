# -*- coding: utf-8 -*-

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException

try:
    from .configuracoes import obter_configuracoes_api
    from .contratos import (
        EntradaConfortoTermico,
        RespostaRaiz,
        RespostaSaude,
        SaidaConfortoTermico,
    )
    from .preditor import Preditor, PreditorPyCaret
except ImportError:
    # Permite executar como subprojeto isolado (python aplicacao.py em src/api).
    from configuracoes import obter_configuracoes_api  # type: ignore
    from contratos import (  # type: ignore
        EntradaConfortoTermico,
        RespostaRaiz,
        RespostaSaude,
        SaidaConfortoTermico,
    )
    from preditor import Preditor, PreditorPyCaret  # type: ignore


def criar_aplicacao(preditor: Preditor | None = None) -> FastAPI:
    configuracoes = obter_configuracoes_api()
    aplicacao = FastAPI(title="API de Conforto Termico", version="1.2.0")
    aplicacao.state.preditor = preditor or PreditorPyCaret(configuracoes.nome_modelo)

    @aplicacao.get("/", response_model=RespostaRaiz)
    def ler_raiz() -> RespostaRaiz:
        return RespostaRaiz.criar_compativel("API de Conforto Termico em execucao!")

    @aplicacao.get("/health", response_model=RespostaSaude)
    def verificar_saude() -> RespostaSaude:
        return RespostaSaude(status="saudavel")

    @aplicacao.post("/predict", response_model=SaidaConfortoTermico)
    def prever(dados: EntradaConfortoTermico) -> SaidaConfortoTermico:
        quadro_dados = pd.DataFrame([dados.model_dump()])
        try:
            rotulo = aplicacao.state.preditor.prever_rotulo(quadro_dados)
        except Exception as erro:
            raise HTTPException(status_code=503, detail=f"Modelo indisponivel: {erro}") from erro
        return SaidaConfortoTermico.criar_compativel(rotulo)

    return aplicacao


aplicacao = criar_aplicacao()


def principal() -> None:
    configuracoes = obter_configuracoes_api()
    uvicorn.run(aplicacao, host=configuracoes.endereco_host, port=configuracoes.porta)


if __name__ == "__main__":
    principal()
