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


class RespostaRaiz(BaseModel):
    """Resposta do endpoint raiz."""

    mensagem: str


class RespostaSaude(BaseModel):
    """Resposta do endpoint de saude."""

    status: str
