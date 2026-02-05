# -*- coding: utf-8 -*-

import os
from typing import Literal

import pandas as pd
import uvicorn
from fastapi import FastAPI
from pycaret.classification import load_model, predict_model
from pydantic import BaseModel

# Create the app
app = FastAPI(title="Thermal Comfort API", version="1.0.0")

# Load trained Pipeline
model = load_model("api")


# Define input/output pydantic models
class ThermalComfortInput(BaseModel):
    idade_anos: int
    peso_kg: float
    altura_cm: int
    sexo_biologico: str
    temperatura_media_c: float
    umidade_relativa_percent: float
    radiacao_solar_media_wm2: float


class ThermalComfortOutput(BaseModel):
    prediction: str


@app.get("/")
def read_root():
    return {"message": "Thermal Comfort API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Define predict function
@app.post("/predict", response_model=ThermalComfortOutput)
def predict(data: ThermalComfortInput):
    data = pd.DataFrame([data.model_dump()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
