from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict

# ============== Servo Schemas ==============

class ServoBase(BaseModel):
    """Schema base para Servo (propiedades en común)"""
    name: str = Field(..., min_length=1, max_length=100)
    pin: int = Field(..., ge=0, le=28)  # GPIO válidos en Raspberry Pi
    min_pulse_width: float = Field(0.0005, ge=0.0001, le=0.001)  # Valor mínimo de pulso en microsegundos
    max_pulse_width: float = Field(0.0025, ge=0.002, le=0.003) # Valor máximo de pulso en microsegundos
    is_active: Optional[bool] = True

class ServoCreate(ServoBase):
    """Schema para crear un Servo"""
    pass

class ServoUpdate(BaseModel):
    """Schema para actualizar un Servo"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    pin: Optional[int] = Field(None, ge=0, le=28)
    min_pulse_width: Optional[float] = Field(None, ge=0.0001, le=0.001)
    max_pulse_width: Optional[float] = Field(None, ge=0.002, le=0.003)
    is_active: Optional[bool] = None

class ServoResponse(ServoBase):
    """Schema para responder con Servo"""
    id: int
    
    class Config:
        from_attributes = True  # Permite leer desde ORM objects


# ============== Motor Reductor Schemas ==============

class MotorReducerBase(BaseModel):
    """Schema base para Motor Reductor (propiedades en común)"""
    name: str = Field(..., min_length=1, max_length=100)
    pin_in1: int = Field(..., ge=0, le=28)
    pin_in2: int = Field(..., ge=0, le=28)
    pin_ena: int = Field(..., ge=0, le=28)
    max_rpm: int = Field(200, ge=50, le=500)  # RPM máximo para conversión de velocidad
    is_active: Optional[bool] = True

class MotorReducerCreate(MotorReducerBase):
    """Schema para crear un Motor Reductor"""
    pass

class MotorReducerUpdate(BaseModel):
    """Schema para actualizar un Motor Reductor"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    gpio_direction_1: Optional[int] = Field(None, ge=0, le=28)
    gpio_direction_2: Optional[int] = Field(None, ge=0, le=28)
    gpio_speed: Optional[int] = Field(None, ge=0, le=28)
    max_rpm: Optional[int] = Field(None, ge=50, le=500)
    is_active: Optional[bool] = None

class MotorReducerResponse(MotorReducerBase):
    """Schema para responder con Motor Reductor"""
    id: int
    
    class Config:
        from_attributes = True


# ============== Camera Preset Schemas ==============

class CameraPresetBase(BaseModel):
    """Schema base para Preset de Cámara (propiedades en común)"""
    name: str = Field(..., min_length=1, max_length=100)
    height: int = Field(..., ge=1)
    width: int = Field(..., ge=1)
    format: str = Field(..., min_length=1, max_length=50)
    is_active: Optional[bool] = True

class CameraPresetCreate(CameraPresetBase):
    """Schema para crear un Preset de Cámara"""
    pass

class CameraPresetUpdate(BaseModel):
    """Schema para actualizar un Preset de Cámara"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    height: Optional[int] = Field(None, ge=1)
    width: Optional[int] = Field(None, ge=1)
    format: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None

class CameraPresetResponse(CameraPresetBase):
    """Schema para responder con Preset de Cámara"""
    id: int
    
    class Config:
        from_attributes = True


# ============== Flow Schemas ==============

class FlowList(BaseModel):
    """Schema para listar Flows"""
    flows_list: List[Dict[str, str]]

class FlowStartRequest(BaseModel):
    """Schema para iniciar un Flow"""
    name: str = Field(..., min_length=1, max_length=100)
    options: dict = Field(..., description="Configuración específica del Flow a iniciar")
    
class FlowSchema(BaseModel):
    """Schema base para Flows"""
    name: str = Field(..., min_length=1, max_length=100)
    beautiful_name: str = Field(..., min_length=1, max_length=100)
    options_schema: Optional[dict] = None
    
class FlowPresetSchema(BaseModel):
    """Esquema para guardar y recuperar presets de la DB"""
    id: Optional[int] = None
    name: str = Field(...)
    flow_name: str = Field(...)
    options: Dict[str, Any]  # Aquí vive el JSON gigante
    is_default: bool = False

    class Config:
        from_attributes = True
    
class FlowPresetUpdate(BaseModel):
    """Schema para actualizar un preset de Flow (solo opciones por ahora)"""
    options: Dict[str, Any] = Field(..., description="Nueva configuración específica del Flow")