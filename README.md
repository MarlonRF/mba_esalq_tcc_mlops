# TCC MLOps - Conforto Termico

Monorepo de MLOps para previsao de conforto termico, com:
- pipelines de processamento e treinamento;
- API FastAPI independente em `src/api`;
- integracao ClearML opcional;
- CI/CD no GitHub Actions com deploy no Cloud Run.

Status atual:
- API em producao: `https://conforto-termico-api-xyuomeiaiq-uc.a.run.app`
- Swagger em producao: `https://conforto-termico-api-xyuomeiaiq-uc.a.run.app/docs`

## Indice

- [Visao Geral](#visao-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Execucao Local](#execucao-local)
- [API REST](#api-rest)
- [ClearML (Opcional)](#clearml-opcional)
- [CI/CD](#cicd)
- [Documentacao](#documentacao)
- [Licenca](#licenca)

## Visao Geral

O projeto foi estruturado para manter modulos desacoplados:
- `src/api`: subprojeto da API (executa sozinho);
- `src/pipelines`, `src/processamento`, `src/treinamento`, `src/features`, `src/utils`: nucleo de ML;
- `src/integracao_clearml`: adaptadores e pipelines com tracking no ClearML (uso opcional).

Convencoes de organizacao:
- `config/`: constantes, dicionarios e configuracoes do projeto;
- `relatorios/`: saidas de testes, cobertura e relatorios gerados;
- `legacy/`: armazenamento temporario de codigo antigo;
- `notebooks/`: prototipagem e execucao local exploratoria.

## Estrutura do Projeto

```text
.
├── config/
├── dados/
├── docs/
├── legacy/
├── notebooks/
├── relatorios/
├── src/
│   ├── api/
│   ├── features/
│   ├── integracao_clearml/
│   ├── pipelines/
│   ├── processamento/
│   ├── treinamento/
│   └── utils/
├── tests/
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
├── pyproject.toml
└── uv.lock
```

## Requisitos

- Python 3.11
- Git
- `uv` (recomendado)
- Docker (para build/teste de imagem da API)

## Instalacao

Na raiz do repositorio:

```bash
uv sync
```

Para ambiente de testes:

```bash
uv sync --extra test
```

Para habilitar integracao ClearML no ambiente local:

```bash
uv sync --extra clearml
```

## Execucao Local

### Testes criticos (sem ClearML)

```bash
uv run python -m pytest tests/unit -m "not clearml" --disable-warnings
```

### API local (subprojeto)

```bash
cd src/api
uv sync
uv run uvicorn aplicacao:aplicacao --host 0.0.0.0 --port 8080
```

Swagger local:
- `http://localhost:8080/docs`

## API REST

Endpoints principais:
- `GET /`
- `GET /health`
- `POST /predict`

Entrada esperada em `POST /predict`:

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

Saida (modo compativel):

```json
{
  "predicao": "Neutro",
  "prediction": "Neutro"
}
```

Variaveis de ambiente da API:
- `API_CAMINHO_MODELO`
- `API_ENDERECO_HOST`
- `API_PORTA`
- `API_COMPAT_LEGADO_ATIVA` (`1`/`0`)
- `API_MODO_CORTE_LEGADO` (`1`/`0`)
- `API_DATA_LIMITE_LEGADO`

## ClearML (Opcional)

A dependencia de ClearML e opcional no projeto.

Quando usar:
- tracking de experimentos;
- versionamento de datasets;
- orquestracao de pipelines com task tracking.

Guia de configuracao:
- `docs/clearml-configuracao.md`

## CI/CD

Workflows:
- `ci.yml`: testes criticos + smoke da API (contrato legado e modo corte);
- `deploy.yml`: deploy no Cloud Run.

Fluxo atual:
- push em `main` dispara CI e deploy de staging;
- deploy em `production` e manual via `workflow_dispatch`;
- deploy em `production` so e permitido:
  - na branch `main`;
  - com `confirmacao_producao=sim`.

Secrets necessarios no GitHub:
- `GCP_PROJECT_ID`
- `GCP_CREDENTIALS`

## Documentacao

Documentos principais em `docs/`:
- `docs/clearml-configuracao.md`
- `docs/api-guia.md`
- `docs/deploy-gcp-setup.md`
- `docs/mlops-setup.md`
- `docs/estrutura-cicd.md`

## Licenca

Projeto licenciado sob MIT. Veja `LICENSE` (quando disponivel no repositorio).
