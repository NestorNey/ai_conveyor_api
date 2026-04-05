# Control de Dispositivos API

API FastAPI para gestionar Servos y Motores Reductores con control GPIO.

## Estructura

```
├── main.py                          # Aplicación principal FastAPI
├── database.py                      # Configuración de BD (SQLite)
├── models.py                        # Modelos SQLAlchemy (Servo, MotorReducer)
├── schemas.py                       # Schemas Pydantic
├── servo_routes.py                  # Rutas de Servos
├── servo_repository.py              # Repositorio CRUD de Servos
├── motor_reducer_routes.py          # Rutas de Motores Reductores
├── motor_reducer_repository.py      # Repositorio CRUD de Motores Reductores
├── test_servo_api.py                # Ejemplos de prueba (Servos)
├── test_motor_reducer_api.py        # Ejemplos de prueba (Motores)
└── README_API.md                    # Esta documentación
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la API:
```bash
python main.py
```

La API estará disponible en: http://localhost:8000

## Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Servo Endpoints

### Crear Servo
```
POST /servos
{
  "name": "servo_principal",
  "gpio": 17,
  "is_active": true
}
```

### Listar todos los Servos
```
GET /servos?skip=0&limit=100
```

### Obtener Servo por ID
```
GET /servos/{servo_id}
```

### Obtener Servo por nombre
```
GET /servos/name/{name}
```

### Obtener Servos activos
```
GET /servos/status/active
```

### Actualizar Servo
```
PUT /servos/{servo_id}
{
  "gpio": 18,
  "is_active": false
}
```

### Eliminar Servo
```
DELETE /servos/{servo_id}
```

---

## Motor Reductor Endpoints

### Crear Motor Reductor
```
POST /motor-reducers
{
  "name": "motor_principal",
  "gpio_direction_1": 17,
  "gpio_direction_2": 27,
  "gpio_speed": 22,
  "is_active": true
}
```

### Listar todos los Motores Reductores
```
GET /motor-reducers?skip=0&limit=100
```

### Obtener Motor Reductor por ID
```
GET /motor-reducers/{motor_id}
```

### Obtener Motor Reductor por nombre
```
GET /motor-reducers/name/{name}
```

### Obtener Motores Reductores activos
```
GET /motor-reducers/status/active
```

### Actualizar Motor Reductor
```
PUT /motor-reducers/{motor_id}
{
  "gpio_speed": 23,
  "is_active": false
}
```

### Eliminar Motor Reductor
```
DELETE /motor-reducers/{motor_id}
```

---

## Modelos

### Servo

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Identificador único |
| name | str | Nombre único del servo |
| gpio | int | Número de GPIO (0-28) |
| is_active | bool | Estado del servo |

### Motor Reductor

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Identificador único |
| name | str | Nombre único |
| gpio_direction_1 | int | GPIO dirección 1 (0-28) |
| gpio_direction_2 | int | GPIO dirección 2 (0-28) |
| gpio_speed | int | GPIO de velocidad PWM (0-28) |
| is_active | bool | Estado del motor |

## Validaciones

- **name:** Requerido, 1-100 caracteres, único
- **gpio_*:** Requerido, entre 0-28 (válidos para Raspberry Pi)
- **is_active:** Opcional, por defecto True

## Errores

- `400 Bad Request` - El nombre ya existe
- `404 Not Found` - Dispositivo no encontrado
- `422 Unprocessable Entity` - Validación fallida

## Modelo Servo

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Identificador único (autoincrement) |
| name | str | Nombre único del servo |
| gpio | int | Número de GPIO (0-28 para RPi) |
| is_active | bool | Estado del servo (activo/inactivo) |

## Validaciones

- **name:** Requerido, 1-100 caracteres, único
- **gpio:** Requerido, entre 0-28 (válidos para Raspberry Pi)
- **is_active:** Opcional, por defecto True

## Errores

- `400 Bad Request` - El nombre ya existe
- `404 Not Found` - Servo no encontrado
- `422 Unprocessable Entity` - Validación fallida
