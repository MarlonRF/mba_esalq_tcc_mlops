# Configuracao ClearML (Opcional)

Este guia padroniza o uso do ClearML no projeto.
A integracao com ClearML e opcional: os pipelines locais e os testes criticos funcionam sem ClearML.

## Quando usar

Use ClearML quando precisar de:
- rastreamento de experimentos;
- versionamento de datasets;
- acompanhamento de artefatos e metricas.

## Pre-requisitos

- Python 3.11
- Dependencias instaladas com extra ClearML:

```bash
uv sync --extra clearml
```

- Conta no ClearML (cloud ou servidor proprio)

## Metodo 1 (recomendado): clearml-init

Execute no terminal:

```bash
clearml-init
```

Informe os dados solicitados (api host, web host, files host, access key e secret key).

Arquivos usuais gerados:
- Windows: `C:\\Users\\<usuario>\\clearml.conf`
- Linux/macOS: `~/.clearml.conf`

## Metodo 2: variaveis de ambiente (.env)

Na raiz do projeto, use `.env`:

```env
CLEARML_API_HOST=https://api.clear.ml
CLEARML_WEB_HOST=https://app.clear.ml
CLEARML_FILES_HOST=https://files.clear.ml
CLEARML_API_ACCESS_KEY=seu_access_key
CLEARML_API_SECRET_KEY=seu_secret_key
```

Observacao:
- nunca commitar credenciais reais;
- use `.env.example` como referencia.

## Validacao rapida

Teste se o ambiente enxerga o pacote:

```bash
uv run python -c "from clearml import Task; print('ClearML OK')"
```

Teste de conexao com criacao de task:

```bash
uv run python -c "from clearml import Task; t=Task.init(project_name='validacao', task_name='teste_conexao', task_type=Task.TaskTypes.testing); print(t.id); t.close()"
```

## Integracao com este projeto

Modulo de integracao:
- `src/integracao_clearml/`

Execucao local sem ClearML:
- continue usando os pipelines em `src/pipelines/` e testes marcados com `not clearml`.

## Problemas comuns

### Credenciais nao encontradas

- Reexecute `clearml-init`; ou
- confirme variaveis no `.env`; ou
- valide o caminho do `clearml.conf`.

### Timeout/erro de conexao

- confirme conectividade com os hosts do ClearML;
- verifique firewall/proxy corporativo.

### Credenciais invalidas

- gere novas chaves no workspace do ClearML;
- atualize `clearml.conf` ou `.env`.

## Seguranca

- Nao commitar chaves.
- Evite compartilhar `clearml.conf`.
- Em CI/CD, preferir secrets do GitHub.
