FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar script de entrada
RUN echo '#!/bin/bash\n\
alembic upgrade head\n\
python seed.py\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]