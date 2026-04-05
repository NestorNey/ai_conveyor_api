from sqlalchemy.orm import Session
from src.models import MotorReducer
from src.schemas import MotorReducerCreate, MotorReducerUpdate
from typing import Optional, List

class MotorReducerRepository:
    """Repositorio para operaciones CRUD de Motor Reductor"""
    
    @staticmethod
    def create(db: Session, motor: MotorReducerCreate) -> MotorReducer:
        """Crear un nuevo Motor Reductor"""
        db_motor = MotorReducer(**motor.dict())
        db.add(db_motor)
        db.commit()
        db.refresh(db_motor)
        return db_motor
    
    @staticmethod
    def get_by_id(db: Session, motor_id: int) -> Optional[MotorReducer]:
        """Obtener Motor Reductor por ID"""
        return db.query(MotorReducer).filter(MotorReducer.id == motor_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[MotorReducer]:
        """Obtener Motor Reductor por nombre"""
        return db.query(MotorReducer).filter(MotorReducer.name == name).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[MotorReducer]:
        """Obtener todos los Motores Reductores con paginación"""
        return db.query(MotorReducer).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, motor_id: int, motor: MotorReducerUpdate) -> Optional[MotorReducer]:
        """Actualizar un Motor Reductor"""
        db_motor = db.query(MotorReducer).filter(MotorReducer.id == motor_id).first()
        if not db_motor:
            return None
        
        # Actualizar solo los campos que tienen valor
        update_data = motor.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_motor, key, value)
        
        db.add(db_motor)
        db.commit()
        db.refresh(db_motor)
        return db_motor
    
    @staticmethod
    def delete(db: Session, motor_id: int) -> bool:
        """Eliminar un Motor Reductor"""
        db_motor = db.query(MotorReducer).filter(MotorReducer.id == motor_id).first()
        if not db_motor:
            return False
        
        db.delete(db_motor)
        db.commit()
        return True
    
    @staticmethod
    def get_active(db: Session) -> List[MotorReducer]:
        """Obtener todos los Motores Reductores activos"""
        return db.query(MotorReducer).filter(MotorReducer.is_active == True).all()
