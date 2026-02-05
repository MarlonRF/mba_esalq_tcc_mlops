FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Dependências de sistema necessárias para PyCaret
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar manifestos de dependências específicos da API
COPY requirements.txt ./

# Instalar dependências Python usando uv (modo pip, sem lock)
RUN pip install --no-cache-dir --upgrade pip uv && \
    uv pip install --system -r requirements.txt

# Copiar código da aplicação
COPY . /app

# Expor porta
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]