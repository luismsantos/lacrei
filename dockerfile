FROM python:3.13-rc-slim as base

# Configurar variáveis de ambiente
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar Poetry
RUN pip install poetry==2.1.2

# Copiar apenas os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Configurar o Poetry para não criar ambiente virtual
RUN poetry config virtualenvs.create false

# Instalar dependências
RUN poetry install --no-interaction --no-ansi

# Copiar o código do projeto
COPY . .

# Expor a porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
