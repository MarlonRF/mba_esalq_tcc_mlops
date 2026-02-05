# Estrutura de diretórios recomendada para CI/CD

/.github/
  /workflows/
    ml-pipeline.yml          # Pipeline principal CI/CD
    data-validation.yml      # Validação de dados
    model-monitoring.yml     # Monitoramento de modelo

/api/
  app.py                     # API FastAPI principal
  requirements.txt           # Dependências da API
  Dockerfile                 # Container da API
  /models/                   # Modelos versionados
  /schemas/                  # Schemas Pydantic
  /tests/                    # Testes da API

/configs/
  processing_config.yaml     # Configuração de processamento
  training_config.yaml       # Configuração de treinamento
  deployment_config.yaml     # Configuração de deploy
  monitoring_config.yaml     # Configuração de monitoramento

/data/
  /raw/                      # Dados brutos (não versionados)
  /processed/                # Dados processados (não versionados)
  /external/                 # Dados externos
  schemas.json               # Schemas de dados

/scripts/
  data_validation.py         # Validação de dados
  model_validation.py        # Validação de modelos
  deploy.py                  # Script de deploy
  monitoring.py              # Script de monitoramento

/tests/
  /unit/                     # Testes unitários
  /integration/              # Testes de integração
  /e2e/                      # Testes end-to-end
  conftest.py                # Configuração pytest
  
/infrastructure/
  /terraform/                # Infraestrutura como código
  /kubernetes/               # Manifests K8s (se usar)
  /monitoring/               # Configurações de monitoramento

/docs/
  api.md                     # Documentação da API
  pipeline.md                # Documentação do pipeline
  deployment.md              # Guia de deployment

# Arquivos de configuração na raiz
requirements.txt             # Dependências do projeto
requirements-dev.txt         # Dependências de desenvolvimento
setup.py                     # Setup do package
pyproject.toml              # Configuração do projeto
.env.example                # Exemplo de variáveis de ambiente
.gitignore                  # Arquivos ignorados pelo Git
.clearml.conf.example       # Exemplo de configuração ClearML
Makefile                    # Comandos úteis
docker-compose.yml          # Para desenvolvimento local