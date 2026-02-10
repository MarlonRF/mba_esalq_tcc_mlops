# 🔐 Configuração do ClearML Online - Guia Completo

Este guia explica **todas as formas** de configurar o ClearML para rastreamento de experimentos online.

---

## 📋 Pré-requisitos

1. Conta no ClearML (gratuita): https://app.clear.ml
2. ClearML instalado: `pip install clearml`

---

## 🎯 Método 1: Via Terminal (RECOMENDADO)

Este é o método **oficial** e mais confiável.

### Passo 1: Obter credenciais

1. Acesse: https://app.clear.ml
2. Faça login
3. Clique no seu nome (canto superior direito) → **Settings**
4. Vá em: **Workspace** → **Create new credentials**
5. Copie os valores exibidos (você vai precisar em breve)

### Passo 2: Configurar no terminal

```bash
# No terminal (PowerShell ou cmd)
clearml-init
```

O comando vai perguntar:

```
ClearML Hosts configuration:
Detect ClearML-server link: (enter)
Web App Host (https://app.clear.ml): [ENTER]
API Host (https://api.clear.ml): [ENTER]  
File Store Host (https://files.clear.ml): [ENTER]

Authentication:
Access Key: [COLE AQUI SEU ACCESS KEY]
Secret Key: [COLE AQUI SEU SECRET KEY]
```

### Passo 3: Verificar

O ClearML cria automaticamente o arquivo `~/clearml.conf` com suas credenciais.

**Pronto!** ✅ Agora pode usar ClearML em qualquer projeto Python.

---

## 🎯 Método 2: Via Arquivo .env (Alternativo)

Use este método se quiser controlar credenciais por projeto.

### Passo 1: Criar arquivo .env

Na **raiz do seu projeto**, crie um arquivo chamado `.env`:

```env
# URLs do servidor ClearML
CLEARML_WEB_HOST=https://app.clear.ml
CLEARML_API_HOST=https://api.clear.ml
CLEARML_FILES_HOST=https://files.clear.ml

# Suas credenciais (obtenha em Settings → Workspace)
CLEARML_API_ACCESS_KEY=SEU_ACCESS_KEY_AQUI
CLEARML_API_SECRET_KEY=SEU_SECRET_KEY_AQUI
```

### Passo 2: Carregar no código

```python
from dotenv import load_dotenv
load_dotenv()

from clearml import Task

# O ClearML vai usar as variáveis de ambiente automaticamente
task = Task.init(project_name='teste', task_name='meu_teste')
task.close()
```

### ⚠️ IMPORTANTE

- **NÃO** faça commit do arquivo `.env` (ele já está no`.gitignore`)
- Use `.env.example` como template seguro

---

## 🎯 Método 3: Programaticamente (Para scripts)

Use este método em scripts automatizados ou ambientes especiais.

```python
from clearml import Task
import os

# Configurar credenciais manualmente
Task.set_credentials(
    api_host='https://api.clear.ml',
    web_host='https://app.clear.ml',
    files_host='https://files.clear.ml',
    key=os.environ.get('CLEARML_API_ACCESS_KEY'),
    secret=os.environ.get('CLEARML_API_SECRET_KEY')
)

# Criar task
task = Task.init(project_name='teste', task_name='meu_teste')
task.close()
```

---

## 🔍 Verificar Configuração

### Método Rápido

```python
from clearml import Task

task = Task.init(project_name='__TESTE__', task_name='teste_conexao')
print(f"✅ Conectado! Task ID: {task.id}")
task.close()
```

Se imprimir o Task ID, está funcionando! 🎉

### Método Completo

Execute o notebook: `notebooks/Notebook_executar_pipelines.ipynb`
- Vá até a seção: **"# ClearML"**
- Execute as células de teste

---

## 🚨 Solução de Problemas

### Erro: "Could not find credentials"

**Causa**: Credenciais não estão configuradas ou foram mal lidas.

**Solução**:
1. Delete o arquivo `~/clearml.conf` (se existir)
2. Execute `clearml-init` novamente
3. Cole as credenciais corretamente

### Erro: "Connection timeout" ou "Remote end closed connection"

**Causa**: Problema de rede/firewall ou servidor sobrecarregado.

**Soluções**:
1. Verifique conexão com internet
2. Tente novamente depois de alguns minutos
3. Use modo offline: `offline_mode=True` nos pipelines
4. Configure proxy (se necessário):
   ```python
   import os
   os.environ['HTTP_PROXY'] = 'http://proxy:port'
   os.environ['HTTPS_PROXY'] = 'http://proxy:port'
   ```

### Erro: Credenciais aparecem mas não conecta

**Causa**: Credenciais podem ter expirado ou sido revogadas.

**Solução**:
1. Acesse: https://app.clear.ml/settings/workspace-configuration
2. Crie **novas** credenciais (revogue as antigas se necessário)
3. Atualize o `.env` ou execute `clearml-init` novamente

### Erro: "Invalid credentials"

**Causa**: Access Key ou Secret Key incorretos.

**Solução**:
1. Verifique se copiou completamente (sem espaços extras)
2. Access Key termina com `==` geralmente
3. Secret Key é muito longo (200+ caracteres)
4. Recrie as credenciais se necessário

---

## 📁 Onde ficam as credenciais?

### Método 1 (clearml-init):
- **Windows**: `C:\Users\SEU_USUARIO\clearml.conf`
- **Linux/Mac**: `~/.clearml.conf`

### Método 2 (.env):
- Na raiz do projeto: `.env`

### Prioridade de leitura:
1. `Task.set_credentials()` (se usado)
2. Variáveis de ambiente (`CLEARML_*`)
3. Arquivo `~/clearml.conf`

---

## 🔒 Segurança

### ✅ Boas práticas:

- Use `.gitignore` para excluir `.env` e `clearml.conf`
- Nunca faça commit de credenciais
- Revogue credenciais antigas ao criar novas
- Use credenciais separadas para produção/desenvolvimento

### ❌ Nunca faça:

- Commit de arquivos com credenciais
- Compartilhar credenciais em chat/email
- Usar mesmas credenciais em múltiplas máquinas sem controle

---

## 🌐 Servidor Own-Hosted

Se estiver usando ClearML Server próprio (não o demo.clear.ml):

```env
CLEARML_WEB_HOST=http://seu-servidor:8080
CLEARML_API_HOST=http://seu-servidor:8008
CLEARML_FILES_HOST=http://seu-servidor:8081

CLEARML_API_ACCESS_KEY=seu_access_key
CLEARML_API_SECRET_KEY=seu_secret_key
```

---

## 📚 Referências

- Documentação oficial: https://clear.ml/docs
- Servidor demo (gratuito): https://app.clear.ml
- GitHub: https://github.com/allegroai/clearml

---

## ✅ Checklist Rápido

Antes de usar ClearML, certifique-se:

- [ ] Conta criada em https://app.clear.ml
- [ ] Credenciais obtidas (Settings → Workspace → Create credentials)
- [ ] `clearml-init` executado no terminal **OU** arquivo `.env` criado
- [ ] Teste de conexão passou (Task.init funcionou)
- [ ] Pode acessar https://app.clear.ml e ver projetos

**Tudo OK?** Você está pronto para usar ClearML! 🚀
