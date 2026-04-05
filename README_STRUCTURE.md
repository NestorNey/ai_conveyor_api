# Control de Dispositivos API

API FastAPI para gestionar Servos y Motores Reductores con control GPIO en Raspberry Pi.

## Estructura del Proyecto

```
prueba_cervos/
├── src/                              # Código principal de la API
│   ├── __init__.py
│   ├── main.py                       # Aplicación FastAPI
│   ├── database.py                   # Configuración de BD
│   ├── models/                       # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py                 # Servlet y MotorReducer
│   ├── schemas/                      # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── schemas.py                # Serialización de datos
│   ├── repositories/                 # Lógica de acceso a datos
│   │   ├── __init__.py
│   │   ├── servo_repository.py       # CRUD Servo
│   │   └── motor_reducer_repository.py # CRUD MotorReducer
│   └── routes/                       # Rutas FastAPI
│       ├── __init__.py
│       ├── servo_routes.py           # Endpoints Servo
│       └── motor_reducer_routes.py   # Endpoints MotorReducer
├── flows/                            # Lógica de flujos (detección, etc)
│   └── flow-1.py
├── env/                              # Virtual environment
├── run.sh                            # Script para ejecutar el servidor
├── dispositivos-api.service          # Archivo de servicio systemctl
├── requirements.txt                  # Dependencias Python
└── README.md                         # Esta documentación
```

## Instalación

### 1. Activar Virtual Environment

```bash
source env/bin/activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Opción 1: Ejecutar manualmente

```bash
./run.sh
```

O directamente:

```bash
source env/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 2: Ejecutar con systemctl (Después)

Copiar el archivo de servicio:
```bash
sudo cp dispositivos-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start dispositivos-api
sudo systemctl enable dispositivos-api  # Para que inicie en el boot
```

Ver estado:
```bash
sudo systemctl status dispositivos-api
sudo journalctl -u dispositivos-api -f  # Ver logs en tiempo real
```

## Documentación de la API

Una vez ejecutada, acceder a:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## Endpoints

### Servos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/servos` | Crear servo |
| GET | `/servos` | Listar todos |
| GET | `/servos/{id}` | Obtener por ID |
| GET | `/servos/name/{name}` | Obtener por nombre |
| GET | `/servos/status/active` | Obtener activos |
| PUT | `/servos/{id}` | Actualizar |
| DELETE | `/servos/{id}` | Eliminar |

### Motores Reductores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/motor-reducers` | Crear motor |
| GET | `/motor-reducers` | Listar todos |
| GET | `/motor-reducers/{id}` | Obtener por ID |
| GET | `/motor-reducers/name/{name}` | Obtener por nombre |
| GET | `/motor-reducers/status/active` | Obtener activos |
| PUT | `/motor-reducers/{id}` | Actualizar |
| DELETE | `/motor-reducers/{id}` | Eliminar |

## Modelos

### Servo

```json
{
  "id": 1,
  "name": "servo_principal",
  "gpio": 17,
  "is_active": true
}
```

### Motor Reductor

```json
{
  "id": 1,
  "name": "motor_principal",
  "gpio_direction_1": 17,
  "gpio_direction_2": 27,
  "gpio_speed": 22,
  "is_active": true
}
```

## Ejemplo de uso

```python
import requests

BASE_URL = "http://localhost:8000"

# Crear un servo
response = requests.post(
    f"{BASE_URL}/servos",
    json={
        "name": "servo_principal",
        "gpio": 17,
        "is_active": True
    }
)
print(response.json())

# Obtener todos los servos
response = requests.get(f"{BASE_URL}/servos")
print(response.json())
```

## Troubleshooting

### El script run.sh no tiene permisos

```bash
chmod +x run.sh
```

### Permissions en systemctl

Asegúrate de que el usuario `josnes` tiene permisos sobre la carpeta del proyecto:

```bash
sudo chown -R josnes:josnes /home/josnes/dev/prueba_cervos
```

### La BD no se crea

El script `run.sh` crea automáticamente la BD en la raíz del proyecto. Si hay problemas, ejecuta directamente:

```bash
python -c "from src.database import engine, Base; from src.models.models import *; Base.metadata.create_all(bind=engine)"
```
