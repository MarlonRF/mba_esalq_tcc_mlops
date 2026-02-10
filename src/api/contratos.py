"""Modelos de contrato da API de conforto termico."""

from pydantic import BaseModel, ConfigDict


class EntradaConfortoTermico(BaseModel):
    """Carga de entrada para predicao em tempo real."""

    model_config = ConfigDict(extra="forbid")

    idade_anos: int
    peso_kg: float
    altura_cm: int
    sexo_biologico: str
    temperatura_media_c: float
    umidade_relativa_percent: float
    radiacao_solar_media_wm2: float


class SaidaConfortoTermico(BaseModel):
    """Carga de saida da predicao."""

    predicao: str
    prediction: str | None = None

    @classmethod
    def criar_compativel(
        cls, predicao: str, incluir_legado: bool = True
    ) -> "SaidaConfortoTermico":
        """Gera resposta com campo novo e legado durante transicao."""
        if incluir_legado:
            return cls(predicao=predicao, prediction=predicao)
        return cls(predicao=predicao)


class RespostaRaiz(BaseModel):
    """Resposta do endpoint raiz."""

    mensagem: str
    message: str | None = None

    @classmethod
    def criar_compativel(
        cls, mensagem: str, incluir_legado: bool = True
    ) -> "RespostaRaiz":
        """Gera resposta com campo novo e legado durante transicao."""
        if incluir_legado:
            return cls(mensagem=mensagem, message=mensagem)
        return cls(mensagem=mensagem)


class RespostaSaude(BaseModel):
    """Resposta do endpoint de saude."""

    status: str
