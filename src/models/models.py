from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class Servo(Base):
    """Modelo SQLAlchemy para Servo"""
    __tablename__ = "servos"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    gpio = Column(Integer, nullable=False)
    min_pulse = Column(Integer, default=500)  # Valor mínimo de pulso en microsegundos
    max_pulse = Column(Integer, default=2500) # Valor máximo de pulso en microsegundos
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Servo(id={self.id}, name={self.name}, gpio={self.gpio})>"


class MotorReducer(Base):
    """Modelo SQLAlchemy para Motor Reductor"""
    __tablename__ = "motor_reducers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    gpio_direction_1 = Column(Integer, nullable=False)
    gpio_direction_2 = Column(Integer, nullable=False)
    gpio_speed = Column(Integer, nullable=False)
    max_rpm = Column(Integer, default=200)  # RPM máximo para conversión de velocidad
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<MotorReducer(id={self.id}, name={self.name}, dir1={self.gpio_direction_1}, dir2={self.gpio_direction_2}, speed={self.gpio_speed})>"
    
class CameraPreset(Base):
    """Modelo SQLAlchemy para Preset de Cámara"""
    __tablename__ = "camera_presets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    format = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<CameraPreset(id={self.id}, name={self.name}, pan={self.pan_angle}, tilt={self.tilt_angle})>"
