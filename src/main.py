import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base, in_memory_db
from src.routes import (
    servo_router, motor_reducer_router, camera_preset_router, 
    flow_router, devices_router, network_router
)
import logging

logger = logging.getLogger(__name__)

# ============ SETUP GPIO PIN FACTORY ============
try:
    from gpiozero import Device
    from gpiozero.pins.lgpio import LGPIOFactory
    
    os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'
    Device.pin_factory = LGPIOFactory()
    logger.info("✅ LGPIOFactory configurado")
except:
    pass

# Cargar los Flows disponibles al iniciar la aplicación
in_memory_db.load_flows()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Control de Dispositivos API",
    description="API para gestionar Servos y Motores Reductores con GPIO",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(servo_router)
app.include_router(motor_reducer_router)
app.include_router(camera_preset_router)
app.include_router(flow_router)
app.include_router(devices_router)
app.include_router(network_router)

@app.get("/", tags=["root"])
def read_root():
    """Endpoint raíz de prueba"""
    return {
        "message": "Control de Dispositivos API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
def health_check():
    """Verificar salud de la API"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
