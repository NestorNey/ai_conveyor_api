#!/bin/bash

# Script para ejecutar la API de Control de Dispositivos con uv
# Uso: ./run.sh

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

export GPIOZERO_PIN_FACTORY=lgpio

# Cambiar al directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv no está instalado${NC}"
    echo -e "${YELLOW}Instala uv con: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi

echo -e "${BLUE}═════════════════════════════════════════${NC}"
echo -e "${GREEN}API Control de Dispositivos${NC}"
echo -e "${BLUE}═════════════════════════════════════════${NC}"

# [NUEVO] Asegurar que el venv exista con acceso a drivers del sistema (libcamera)
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[0/3] Creando entorno virtual con acceso a drivers del sistema...${NC}"
    uv venv --system-site-packages
fi

# Instalar dependencias si es necesario
echo -e "${YELLOW}[1/3] Verificando dependencias...${NC}"
# Usamos uv sync para asegurar que josneslib y picamera2 estén listos
uv sync --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias listas${NC}"
else
    echo -e "${RED}❌ Error al sincronizar dependencias${NC}"
    exit 1
fi

# Crear la tabla de BD si no existe
echo -e "${YELLOW}[2/3] Inicializando base de datos...${NC}"
# Ejecutamos con uv run para usar el venv recién verificado
uv run python -c "from src.database import engine, Base; from src.models.models import *; Base.metadata.create_all(bind=engine)"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos lista${NC}"
else
    echo -e "${YELLOW}⚠️ Base de datos ya existe o información de modelos${NC}"
fi

# Iniciar el servidor
echo -e "${YELLOW}[3/3] Iniciando servidor...${NC}"
echo ""
echo -e "${GREEN}🚀 Servidor corriendo en: ${BLUE}http://0.0.0.0:8000${NC}"
echo -e "${GREEN}📚 Documentación en: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "${GREEN}🎥 Viewer de cámara en: ${BLUE}http://localhost:8000/flows/viewer${NC}"
echo ""
echo -e "${YELLOW}Presiona Ctrl+C para detener el servidor${NC}"
echo ""

# Ejecutar con uv (usará automáticamente el venv con acceso a libcamera)
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload