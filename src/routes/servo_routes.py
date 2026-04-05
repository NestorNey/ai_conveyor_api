from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.schemas import ServoCreate, ServoUpdate, ServoResponse
from src.repositories.servo_repository import ServoRepository
from typing import List

router = APIRouter(prefix="/servos", tags=["servos"])

@router.post("/", response_model=ServoResponse, status_code=status.HTTP_201_CREATED)
def create_servo(servo: ServoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo Servo"""
    # Verificar si el nombre ya existe
    existing = ServoRepository.get_by_name(db, servo.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Servo con nombre '{servo.name}' ya existe"
        )
    
    return ServoRepository.create(db, servo)

@router.get("/{servo_id}", response_model=ServoResponse)
def get_servo(servo_id: int, db: Session = Depends(get_db)):
    """Obtener un Servo por ID"""
    servo = ServoRepository.get_by_id(db, servo_id)
    if not servo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servo con ID {servo_id} no encontrado"
        )
    return servo

@router.get("/name/{name}", response_model=ServoResponse)
def get_servo_by_name(name: str, db: Session = Depends(get_db)):
    """Obtener un Servo por nombre"""
    servo = ServoRepository.get_by_name(db, name)
    if not servo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servo con nombre '{name}' no encontrado"
        )
    return servo

@router.get("/", response_model=List[ServoResponse])
def list_servos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los Servos con paginación"""
    servos = ServoRepository.get_all(db, skip, limit)
    return servos

@router.get("/status/active", response_model=List[ServoResponse])
def get_active_servos(db: Session = Depends(get_db)):
    """Obtener todos los Servos activos"""
    servos = ServoRepository.get_active(db)
    return servos

@router.put("/{servo_id}", response_model=ServoResponse)
def update_servo(servo_id: int, servo: ServoUpdate, db: Session = Depends(get_db)):
    """Actualizar un Servo"""
    updated_servo = ServoRepository.update(db, servo_id, servo)
    if not updated_servo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servo con ID {servo_id} no encontrado"
        )
    return updated_servo

@router.delete("/{servo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servo(servo_id: int, db: Session = Depends(get_db)):
    """Eliminar un Servo"""
    success = ServoRepository.delete(db, servo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servo con ID {servo_id} no encontrado"
        )
    return None
