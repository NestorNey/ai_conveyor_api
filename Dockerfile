# Dockerfile para AI Conveyor API
FROM python:3.11-slim-bullseye

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libopenjp2-7 \
    libtiff5 \
    libjasper1 \
    libharfbuzz0b \
    libwebp6 \
    libopenblas-dev \
    libjasper-dev \
    libatlas-base-dev \
    libharfbuzz-dev \
    libwebp-dev \
    libtiff-dev \
    libjasper-dev \
    pkg-config \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv (gestor de paquetes Python rápido)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copiar archivos del proyecto
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY settings.py ./
COPY requirements.txt ./

# Crear venv y instalar dependencias
RUN /root/.cargo/bin/uv venv --python python3.11
ENV PATH="/app/.venv/bin:$PATH"
RUN /root/.cargo/bin/uv sync

# Copiar los flows
COPY flows ./flows

# Crear directorio para db
RUN mkdir -p /app/data

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/docs', timeout=5)"

# Comando para iniciar la API
CMD ["/root/.cargo/bin/uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
