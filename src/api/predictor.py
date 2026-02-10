"""
Prediction runtime abstractions for the API.
"""

from typing import Any, Protocol

import pandas as pd


class Predictor(Protocol):
    def predict_label(self, data: pd.DataFrame) -> str:
        """Return one prediction label for one-row dataframe."""


class PyCaretPredictor:
    """Thin adapter around PyCaret model loading/prediction."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self._model: Any = None

    def _ensure_model(self) -> None:
        if self._model is not None:
            return

        from pycaret.classification import load_model

        self._model = load_model(self.model_name)

    def predict_label(self, data: pd.DataFrame) -> str:
        self._ensure_model()

        from pycaret.classification import predict_model

        predictions = predict_model(self._model, data=data)
        return str(predictions["prediction_label"].iloc[0])

