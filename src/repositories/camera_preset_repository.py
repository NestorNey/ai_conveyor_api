from sqlalchemy.orm import Session
from src.models import CameraPreset
from src.schemas import CameraPresetCreate, CameraPresetUpdate
from typing import Optional, List

class CameraPresetRepository:
    """Repositorio para operaciones CRUD de Preset de Cámara"""
    
    @staticmethod
    def create(db: Session, preset: CameraPresetCreate) -> CameraPreset:
        """Crear un nuevo Preset de Cámara"""
        db_preset = CameraPreset(**preset.dict())
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        return db_preset
    
    @staticmethod
    def get_by_id(db: Session, preset_id: int) -> Optional[CameraPreset]:
        """Obtener Preset de Cámara por ID"""
        return db.query(CameraPreset).filter(CameraPreset.id == preset_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[CameraPreset]:
        """Obtener Preset de Cámara por nombre"""
        return db.query(CameraPreset).filter(CameraPreset.name == name).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CameraPreset]:
        """Obtener todos los Presets de Cámara con paginación"""
        return db.query(CameraPreset).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, preset_id: int, preset: CameraPresetUpdate) -> Optional[CameraPreset]:
        """Actualizar un Preset de Cámara"""
        db_preset = db.query(CameraPreset).filter(CameraPreset.id == preset_id).first()
        if not db_preset:
            return None
        
        # Actualizar solo los campos que tienen valor
        update_data = preset.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_preset, key, value)
        
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        return db_preset
    
    @staticmethod
    def delete(db: Session, preset_id: int) -> bool:
        """Eliminar un Preset de Cámara"""
        db_preset = db.query(CameraPreset).filter(CameraPreset.id == preset_id).first()
        if not db_preset:
            return False
        
        db.delete(db_preset)
        db.commit()
        return True