# Thermal Comfort API (Subproject)

This folder is a standalone API project inside the monorepo.
It can run independently from pipelines while still consuming the trained model artifact.

## Architecture

- `app.py`: FastAPI application factory and routes
- `contracts.py`: request/response contract (Pydantic)
- `predictor.py`: prediction adapter (PyCaret runtime)
- `settings.py`: runtime settings and model path resolution

## Interface Contract

### `POST /predict` input

```json
{
  "idade_anos": 30,
  "peso_kg": 70.0,
  "altura_cm": 175,
  "sexo_biologico": "m",
  "temperatura_media_c": 25.0,
  "umidade_relativa_percent": 60.0,
  "radiacao_solar_media_wm2": 400.0
}
```

### `POST /predict` output

```json
{
  "prediction": "Neutro"
}
```

## Run locally (subproject mode)

```powershell
cd src/api
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 8080
```

## Environment variables

- `API_MODEL_PATH`: path/basename for model file (with or without `.pkl`)
- `API_HOST`: API bind host (default `0.0.0.0`)
- `API_PORT` or `PORT`: API bind port (default `8080`)

## Docker

Build from repository root:

```powershell
docker build -t conforto-api-local -f src/api/Dockerfile src/api
docker run -d --name conforto-api -p 8080:8080 conforto-api-local
```

## Manual request (PowerShell)

```powershell
$payload = @{
  idade_anos = 30
  peso_kg = 70.0
  altura_cm = 175
  sexo_biologico = "m"
  temperatura_media_c = 25.0
  umidade_relativa_percent = 60.0
  radiacao_solar_media_wm2 = 400.0
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8080/predict -Method POST -ContentType "application/json" -Body $payload
```

