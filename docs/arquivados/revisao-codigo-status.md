# 📋 Revisão de Código - Projeto Conforto Térmico

## 🏗️ **Reorganização da Estrutura**

### Movimentação de Arquivos de Documentação
✅ **Concluído**: Todos os arquivos `.md` foram movidos para a pasta `documentacao/`:
- `docs/` → `documentacao/`
- `api/README.md` → `documentacao/api-guia.md`
- `MLOPS-QUICKSTART.md` → `documentacao/`
- Mantido apenas `README.md` na raiz

## 🔧 **Refatoração de Código**

### 1. Pipeline Utils (`funcoes/pipeline_utils.py`)
✅ **Concluído - Totalmente Refatorado**:

#### Funções Renomeadas e Documentadas:
- `ensure_group_column()` → `garantir_coluna_agrupamento_temporal()`
- `safe_preprocess()` → `executar_preprocessamento_seguro()`  
- `resolve_columns_local()` → `resolver_nomes_colunas_locais()`
- `resolve_columns()` → `resolver_nomes_colunas()`
- `resolve_target_col()` → `resolver_coluna_alvo()`

#### Melhorias Implementadas:
- ✅ Nomes de variáveis em português
- ✅ Comentários linha a linha descrevendo a lógica
- ✅ Docstrings completas com Args, Returns e Examples
- ✅ Type hints atualizados
- ✅ Documentação do módulo adicionada

### 2. Processamento (`funcoes/processamento.py`)
🔄 **Em Andamento - Parcialmente Refatorado**:

#### Já Refatorado:
- ✅ Cabeçalho do arquivo com documentação completa
- ✅ `ProcCfg` → `ConfiguracaoProcessamento` (com documentação detalhada)
- ✅ Funções utilitárias internas renomeadas:
  - `_to_float()` → `_converter_para_float()`
  - `_ensure_dir()` → `_garantir_diretorio_existe()`
  - `_label_encode()` → `_codificar_com_labels()`
  - `_heat_index()` → `_calcular_indice_calor()`
  - `_dew_point()` → `_calcular_ponto_orvalho()`
  - `_imc()` → `_calcular_imc()`

#### Pendente:
- 🔄 Atualizar referências às funções renomeadas nas funções principais
- 🔄 Refatorar funções principais (`processar_df`, `processar_arquivo`)
- 🔄 Atualizar nomes de variáveis para português
- 🔄 Adicionar comentários detalhados nas funções principais

### 3. Outros Arquivos Pendentes:
- 📝 `funcoes/analise_exploratoria.py`
- 📝 `funcoes/clearml_project.py`
- 📝 `funcoes/gerar_dados.py` 
- 📝 `funcoes/io_clearml.py`
- 📝 `funcoes/io_local.py`
- 📝 `funcoes/treinar.py`
- 📝 `api/app.py`

## 📊 **Status da Revisão**

### ✅ **Concluído (30%)**
- Organização da documentação
- `pipeline_utils.py` totalmente refatorado
- Estrutura base do `processamento.py`

### 🔄 **Em Andamento (20%)**
- `processamento.py` - funções principais pendentes

### 📝 **Pendente (50%)**
- Demais arquivos em `funcoes/`
- API Flask/FastAPI
- Atualização de imports onde necessário

## 📋 **Próximos Passos**

### Prioridade Alta:
1. **Finalizar `processamento.py`**:
   - Corrigir referências às funções renomeadas
   - Refatorar função `processar_df()`
   - Refatorar função `processar_arquivo()`

2. **Revisar `treinar.py`**:
   - Funcões de treinamento de modelos
   - Integração com ClearML

3. **Revisar `api/app.py`**:
   - Endpoints da API
   - Validação de dados
   - Tratamento de erros

### Prioridade Média:
4. **Arquivos de I/O**:
   - `io_local.py` e `io_clearml.py`
   - Funções de leitura/escrita

5. **Análise exploratória**:
   - `analise_exploratoria.py`
   - Funções de visualização

### Prioridade Baixa:
6. **Utilitários**:
   - `gerar_dados.py`
   - `clearml_project.py`

## 🎯 **Padrões de Nomenclatura Estabelecidos**

### Variáveis:
- **Português**: `dataframe_entrada`, `configuracao_alvo`
- **Snake_case**: `nome_variavel_composta`
- **Descritivos**: `lista_colunas_numericas` vs `cols`

### Funções:
- **Português**: `calcular_imc()`, `resolver_colunas()`
- **Verbos**: `garantir_`, `executar_`, `processar_`
- **Descritivas**: Nome indica claramente o que faz

### Documentação:
- **Docstrings**: Sempre com Args, Returns, Examples quando relevante
- **Comentários**: Linha a linha explicando lógica complexa
- **Type Hints**: Sempre presentes

---
**Atualizado**: 28 de setembro de 2025  
**Status**: Revisão em andamento