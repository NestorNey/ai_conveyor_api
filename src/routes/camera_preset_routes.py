from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import CameraPresetCreate, CameraPresetUpdate, CameraPresetResponse
from src.repositories import CameraPresetRepository
from typing import List

router = APIRouter(prefix="/camera-presets", tags=["camera-presets"])

@router.post("/", response_model=CameraPresetResponse, status_code=status.HTTP_201_CREATED)
def create_camera_preset(preset: CameraPresetCreate, db: Session = Depends(get_db)):
    """Crear un nuevo Preset de Cámara"""
    # Verificar si el nombre ya existe
    existing = CameraPresetRepository.get_by_name(db, preset.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Preset de Cámara con nombre '{preset.name}' ya existe"
        )
    
    return CameraPresetRepository.create(db, preset)

@router.get("/{preset_id}", response_model=CameraPresetResponse)
def get_camera_preset(preset_id: int, db: Session = Depends(get_db)):
    """Obtener un Preset de Cámara por ID"""
    preset = CameraPresetRepository.get_by_id(db, preset_id)
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset de Cámara con ID {preset_id} no encontrado"
        )
    return preset

@router.get("/name/{name}", response_model=CameraPresetResponse)
def get_camera_preset_by_name(name: str, db: Session = Depends(get_db)):
    """Obtener un Preset de Cámara por nombre"""
    preset = CameraPresetRepository.get_by_name(db, name)
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset de Cámara con nombre '{name}' no encontrado"
        )
    return preset

@router.get("/", response_model=List[CameraPresetResponse])
def list_camera_presets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los Presets de Cámara con paginación"""
    presets = CameraPresetRepository.get_all(db, skip, limit)
    return presets

@router.put("/{preset_id}", response_model=CameraPresetResponse)
def update_camera_preset(preset_id: int, preset: CameraPresetUpdate, db: Session = Depends(get_db)):
    """Actualizar un Preset de Cámara"""
    updated_preset = CameraPresetRepository.update(db, preset_id, preset)
    if not updated_preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset de Cámara con ID {preset_id} no encontrado"
        )
    return updated_preset

@router.delete("/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera_preset(preset_id: int, db: Session = Depends(get_db)):
    """Eliminar un Preset de Cámara"""
    success = CameraPresetRepository.delete(db, preset_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset de Cámara con ID {preset_id} no encontrado"
        )
    return None