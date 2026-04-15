# Usamos una imagen de Python oficial
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y forzar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias de sistema necesarias para RPi.GPIO y compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libcamera-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv para manejar las dependencias rápido
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# 1. Copiamos la LIBRERÍA e instalamos como paquete real (no editable)
COPY ai_conveyor_lib /app/ai_conveyor_lib
RUN uv pip install --system /app/ai_conveyor_lib

# 2. Copiamos la API
COPY ai_conveyor_api /app/ai_conveyor_api
WORKDIR /app/ai_conveyor_api

# 3. Instalamos las dependencias de la API
# Como ya instalamos josneslib arriba, uv detectará que ya está satisfecha
RUN uv pip install --system .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando de producción (sin --reload)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]