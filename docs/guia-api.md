# API de Conforto Termico

Guia padronizado da API FastAPI em `src/api`, tratada como subprojeto independente dentro do monorepo.

## Visao geral

- Codigo da API: `src/api`
- App principal: `src/api/aplicacao.py`
- Contratos (entrada/saida): `src/api/contratos.py`
- Configuracoes: `src/api/configuracoes.py`
- Preditor: `src/api/preditor.py`

## Execucao local

```bash
cd src/api
uv sync
uv run uvicorn aplicacao:aplicacao --host 0.0.0.0 --port 8080
```

Swagger local:
- `http://localhost:8080/docs`

## Docker

Build na raiz do repositorio:

```bash
docker build -t conforto-api-local -f src/api/Dockerfile src/api
docker run --rm -p 8080:8080 conforto-api-local
```

## Endpoints

- `GET /`
- `GET /health`
- `POST /predict`

### Exemplo de entrada (`POST /predict`)

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

### Exemplo de saida (modo compativel)

```json
{
  "predicao": "Neutro",
  "prediction": "Neutro"
}
```

## Compatibilidade de contrato

Campos oficiais:
- `predicao` (POST `/predict`)
- `mensagem` (GET `/`)

Campos legados (temporarios):
- `prediction`
- `message`

Cabecalhos de transicao:
- `X-Compatibilidade-Legado` (`ativa`/`inativa`)
- `X-Modo-Corte-Legado` (`ativo`/`inativo`)
- `X-Data-Limite-Legado`

## Variaveis de ambiente

- `API_CAMINHO_MODELO`
- `API_ENDERECO_HOST` (padrao `0.0.0.0`)
- `API_PORTA` (padrao `8080`)
- `API_COMPAT_LEGADO_ATIVA` (`1`/`0`)
- `API_MODO_CORTE_LEGADO` (`1`/`0`)
- `API_DATA_LIMITE_LEGADO`

Compatibilidade mantida:
- `API_MODEL_PATH`
- `API_HOST`
- `API_PORT`
- `PORT`

## Producao

- URL API: `https://conforto-termico-api-xyuomeiaiq-uc.a.run.app`
- Swagger: `https://conforto-termico-api-xyuomeiaiq-uc.a.run.app/docs`

## Troubleshooting rapido

### API sobe, mas modelo nao carrega

- confirme caminho de modelo em `API_CAMINHO_MODELO`;
- confirme arquivo de modelo no container/imagem.

### Erro 422 no `/predict`

- confira nomes e tipos dos campos no JSON;
- valide payload pelo Swagger em `/docs`.

### Erro 403 em Cloud Run

- revise politica de invoker no servico;
- valide permissao publica quando `--allow-unauthenticated` for esperado.
