# -*- coding: utf-8 -*-

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException

try:
    from .contracts import (
        HealthResponse,
        RootResponse,
        ThermalComfortInput,
        ThermalComfortOutput,
    )
    from .predictor import Predictor, PyCaretPredictor
    from .settings import get_api_settings
except ImportError:
    # Allow running as a standalone project (python app.py from src/api).
    from contracts import (  # type: ignore
        HealthResponse,
        RootResponse,
        ThermalComfortInput,
        ThermalComfortOutput,
    )
    from predictor import Predictor, PyCaretPredictor  # type: ignore
    from settings import get_api_settings  # type: ignore


def create_app(predictor: Predictor | None = None) -> FastAPI:
    settings = get_api_settings()
    app = FastAPI(title="Thermal Comfort API", version="1.1.0")
    app.state.predictor = predictor or PyCaretPredictor(settings.model_name)

    @app.get("/", response_model=RootResponse)
    def read_root() -> RootResponse:
        return RootResponse(message="Thermal Comfort API is running!")

    @app.get("/health", response_model=HealthResponse)
    def health_check() -> HealthResponse:
        return HealthResponse(status="healthy")

    @app.post("/predict", response_model=ThermalComfortOutput)
    def predict(data: ThermalComfortInput) -> ThermalComfortOutput:
        frame = pd.DataFrame([data.model_dump()])
        try:
            label = app.state.predictor.predict_label(frame)
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Model unavailable: {exc}") from exc
        return ThermalComfortOutput(prediction=label)

    return app


app = create_app()


def main() -> None:
    settings = get_api_settings()
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
