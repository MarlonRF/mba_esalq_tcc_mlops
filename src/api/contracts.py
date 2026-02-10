"""
Contract models for the Thermal Comfort API.
"""

from pydantic import BaseModel, ConfigDict


class ThermalComfortInput(BaseModel):
    """Input payload for real-time prediction."""

    model_config = ConfigDict(extra="forbid")

    idade_anos: int
    peso_kg: float
    altura_cm: int
    sexo_biologico: str
    temperatura_media_c: float
    umidade_relativa_percent: float
    radiacao_solar_media_wm2: float


class ThermalComfortOutput(BaseModel):
    """Prediction response payload."""

    prediction: str


class RootResponse(BaseModel):
    """Root endpoint response."""

    message: str


class HealthResponse(BaseModel):
    """Health endpoint response."""

    status: str

