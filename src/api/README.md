# API de Conforto Termico (Subprojeto)

Esta pasta funciona como subprojeto independente dentro do monorepo.
Ela pode ser executada separadamente dos pipelines, consumindo apenas o artefato do modelo treinado.

## Arquitetura

- `aplicacao.py`: fabrica da aplicacao FastAPI e rotas
- `contratos.py`: contrato de entrada e saida (Pydantic)
- `preditor.py`: adaptador de predicao (runtime PyCaret)
- `configuracoes.py`: leitura de configuracoes e resolucao do caminho do modelo

## Contrato de Interface

### Entrada `POST /predict`

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

### Saida `POST /predict`

```json
{
  "predicao": "Neutro",
  "prediction": "Neutro"
}
```

Compatibilidade temporaria:
- `predicao`: campo oficial atual
- `prediction`: campo legado para clientes antigos
- `mensagem`: campo oficial atual no endpoint `/`
- `message`: campo legado para clientes antigos no endpoint `/`

Politica de corte:
- data limite padrao para campos legados: `2026-06-30`
- variavel para manter/desligar legado: `API_COMPAT_LEGADO_ATIVA` (`1`/`0`)
- recomendacao: homologacao com `API_COMPAT_LEGADO_ATIVA=0` antes do corte em producao

## Execucao local (modo subprojeto)

```powershell
cd src/api
uv sync
uv run uvicorn aplicacao:aplicacao --host 0.0.0.0 --port 8080
```

## Variaveis de ambiente

- `API_CAMINHO_MODELO`: caminho/base do arquivo de modelo (com ou sem `.pkl`)
- `API_ENDERECO_HOST`: host de bind da API (padrao `0.0.0.0`)
- `API_PORTA`: porta da API (padrao `8080`)
- `API_COMPAT_LEGADO_ATIVA`: ativa/desativa campos legados (`1` por padrao)
- `API_DATA_LIMITE_LEGADO`: data informativa de retirada do legado (`2026-06-30`)

Compatibilidade mantida:
- `API_MODEL_PATH`
- `API_HOST`
- `API_PORT`
- `PORT`

## Docker

Build a partir da raiz do repositorio:

```powershell
docker build -t conforto-api-local -f src/api/Dockerfile src/api
docker run -d --name conforto-api -p 8080:8080 conforto-api-local
```

## Requisicao manual (PowerShell)

```powershell
$corpo = @{
  idade_anos = 30
  peso_kg = 70.0
  altura_cm = 175
  sexo_biologico = "m"
  temperatura_media_c = 25.0
  umidade_relativa_percent = 60.0
  radiacao_solar_media_wm2 = 400.0
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8080/predict -Method POST -ContentType "application/json" -Body $corpo
```
