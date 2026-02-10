"""
Configuration utilities for the API runtime.
"""

import os
from dataclasses import dataclass
from pathlib import Path


def _strip_pkl_suffix(model_path: str) -> str:
    if model_path.endswith(".pkl"):
        return model_path[:-4]
    return model_path


def _resolve_model_name() -> str:
    env_value = os.environ.get("API_MODEL_PATH")
    if env_value:
        return _strip_pkl_suffix(env_value)

    candidates = [
        Path("api"),  # repo root execution (expects api.pkl)
        Path(__file__).resolve().parent / "api",  # src/api/api.pkl
        Path("/app/api"),  # Docker default workdir
    ]

    for candidate in candidates:
        if candidate.with_suffix(".pkl").exists():
            return str(candidate)

    return "api"


@dataclass(frozen=True)
class ApiSettings:
    host: str
    port: int
    model_name: str


def get_api_settings() -> ApiSettings:
    return ApiSettings(
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", os.environ.get("API_PORT", "8080"))),
        model_name=_resolve_model_name(),
    )

