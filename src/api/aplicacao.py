# -*- coding: utf-8 -*-

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Response

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


def aplicar_cabecalhos_transicao(
    resposta_http: Response,
    compatibilidade_legado_ativa: bool,
    modo_corte_legado_ativo: bool,
    data_limite_legado: str,
) -> None:
    """Inclui cabecalhos para orientar clientes na transicao de contrato."""
    resposta_http.headers["X-Compatibilidade-Legado"] = (
        "ativa" if compatibilidade_legado_ativa else "inativa"
    )
    resposta_http.headers["X-Modo-Corte-Legado"] = (
        "ativo" if modo_corte_legado_ativo else "inativo"
    )
    resposta_http.headers["X-Data-Limite-Legado"] = data_limite_legado


def criar_aplicacao(preditor: Preditor | None = None) -> FastAPI:
    configuracoes = obter_configuracoes_api()
    aplicacao = FastAPI(title="API de Conforto Termico", version="1.3.0")
    aplicacao.state.preditor = preditor or PreditorPyCaret(configuracoes.nome_modelo)

    @aplicacao.get("/", response_model=RespostaRaiz, response_model_exclude_none=True)
    def ler_raiz(resposta_http: Response) -> RespostaRaiz:
        aplicar_cabecalhos_transicao(
            resposta_http,
            configuracoes.compatibilidade_legado_ativa,
            configuracoes.modo_corte_legado_ativo,
            configuracoes.data_limite_legado,
        )
        return RespostaRaiz.criar_compativel(
            "API de Conforto Termico em execucao!",
            incluir_legado=configuracoes.compatibilidade_legado_ativa,
        )

    @aplicacao.get("/health", response_model=RespostaSaude)
    def verificar_saude() -> RespostaSaude:
        return RespostaSaude(status="saudavel")

    @aplicacao.post(
        "/predict", response_model=SaidaConfortoTermico, response_model_exclude_none=True
    )
    def prever(dados: EntradaConfortoTermico, resposta_http: Response) -> SaidaConfortoTermico:
        quadro_dados = pd.DataFrame([dados.model_dump()])
        try:
            rotulo = aplicacao.state.preditor.prever_rotulo(quadro_dados)
        except Exception as erro:
            raise HTTPException(status_code=503, detail=f"Modelo indisponivel: {erro}") from erro
        aplicar_cabecalhos_transicao(
            resposta_http,
            configuracoes.compatibilidade_legado_ativa,
            configuracoes.modo_corte_legado_ativo,
            configuracoes.data_limite_legado,
        )
        return SaidaConfortoTermico.criar_compativel(
            rotulo, incluir_legado=configuracoes.compatibilidade_legado_ativa
        )

    return aplicacao


aplicacao = criar_aplicacao()


def principal() -> None:
    configuracoes = obter_configuracoes_api()
    uvicorn.run(aplicacao, host=configuracoes.endereco_host, port=configuracoes.porta)


if __name__ == "__main__":
    principal()
