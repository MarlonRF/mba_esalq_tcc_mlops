"""Abstracoes de execucao de predicao para a API."""

from typing import Any, Protocol

import pandas as pd


class Preditor(Protocol):
    def prever_rotulo(self, dados: pd.DataFrame) -> str:
        """Retorna um rotulo previsto para um dataframe de uma linha."""


class PreditorPyCaret:
    """Adaptador para carregamento e predicao com PyCaret."""

    def __init__(self, nome_modelo: str):
        self.nome_modelo = nome_modelo
        self._modelo: Any = None

    def _garantir_modelo(self) -> None:
        if self._modelo is not None:
            return

        from pycaret.classification import load_model

        self._modelo = load_model(self.nome_modelo)

    def prever_rotulo(self, dados: pd.DataFrame) -> str:
        self._garantir_modelo()

        from pycaret.classification import predict_model

        previsoes = predict_model(self._modelo, data=dados)
        return str(previsoes["prediction_label"].iloc[0])
