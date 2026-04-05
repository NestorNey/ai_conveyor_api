from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import MotorReducerCreate, MotorReducerUpdate, MotorReducerResponse
from src.repositories import MotorReducerRepository
from typing import List

router = APIRouter(prefix="/motor-reducers", tags=["motor-reducers"])

@router.post("/", response_model=MotorReducerResponse, status_code=status.HTTP_201_CREATED)
def create_motor_reducer(motor: MotorReducerCreate, db: Session = Depends(get_db)):
    """Crear un nuevo Motor Reductor"""
    # Verificar si el nombre ya existe
    existing = MotorReducerRepository.get_by_name(db, motor.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Motor Reductor con nombre '{motor.name}' ya existe"
        )
    
    return MotorReducerRepository.create(db, motor)

@router.get("/{motor_id}", response_model=MotorReducerResponse)
def get_motor_reducer(motor_id: int, db: Session = Depends(get_db)):
    """Obtener un Motor Reductor por ID"""
    motor = MotorReducerRepository.get_by_id(db, motor_id)
    if not motor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motor Reductor con ID {motor_id} no encontrado"
        )
    return motor

@router.get("/name/{name}", response_model=MotorReducerResponse)
def get_motor_reducer_by_name(name: str, db: Session = Depends(get_db)):
    """Obtener un Motor Reductor por nombre"""
    motor = MotorReducerRepository.get_by_name(db, name)
    if not motor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motor Reductor con nombre '{name}' no encontrado"
        )
    return motor

@router.get("/", response_model=List[MotorReducerResponse])
def list_motor_reducers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los Motores Reductores con paginación"""
    motors = MotorReducerRepository.get_all(db, skip, limit)
    return motors

@router.get("/status/active", response_model=List[MotorReducerResponse])
def get_active_motor_reducers(db: Session = Depends(get_db)):
    """Obtener todos los Motores Reductores activos"""
    motors = MotorReducerRepository.get_active(db)
    return motors

@router.put("/{motor_id}", response_model=MotorReducerResponse)
def update_motor_reducer(motor_id: int, motor: MotorReducerUpdate, db: Session = Depends(get_db)):
    """Actualizar un Motor Reductor"""
    updated_motor = MotorReducerRepository.update(db, motor_id, motor)
    if not updated_motor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motor Reductor con ID {motor_id} no encontrado"
        )
    return updated_motor

@router.delete("/{motor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_motor_reducer(motor_id: int, db: Session = Depends(get_db)):
    """Eliminar un Motor Reductor"""
    success = MotorReducerRepository.delete(db, motor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motor Reductor con ID {motor_id} no encontrado"
        )
    return None
