from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# ============== Servo Schemas ==============

class ServoBase(BaseModel):
    """Schema base para Servo (propiedades en común)"""
    name: str = Field(..., min_length=1, max_length=100)
    gpio: int = Field(..., ge=0, le=28)  # GPIO válidos en Raspberry Pi
    min_pulse: int = Field(500, ge=100, le=1000)  # Valor mínimo de pulso en microsegundos
    max_pulse: int = Field(2500, ge=2000, le=3000) # Valor máximo de pulso en microsegundos
    is_active: Optional[bool] = True

class ServoCreate(ServoBase):
    """Schema para crear un Servo"""
    pass

class ServoUpdate(BaseModel):
    """Schema para actualizar un Servo"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    gpio: Optional[int] = Field(None, ge=0, le=28)
    min_pulse: Optional[int] = Field(None, ge=100, le=1000)
    max_pulse: Optional[int] = Field(None, ge=2000, le=3000)
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
    gpio_direction_1: int = Field(..., ge=0, le=28)
    gpio_direction_2: int = Field(..., ge=0, le=28)
    gpio_speed: int = Field(..., ge=0, le=28)
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