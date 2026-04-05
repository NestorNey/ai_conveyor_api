from sqlalchemy.orm import Session
from src.models import Servo
from src.schemas import ServoCreate, ServoUpdate
from typing import Optional, List

class ServoRepository:
    """Repositorio para operaciones CRUD de Servo"""
    
    @staticmethod
    def create(db: Session, servo: ServoCreate) -> Servo:
        """Crear un nuevo Servo"""
        db_servo = Servo(**servo.dict())
        db.add(db_servo)
        db.commit()
        db.refresh(db_servo)
        return db_servo
    
    @staticmethod
    def get_by_id(db: Session, servo_id: int) -> Optional[Servo]:
        """Obtener Servo por ID"""
        return db.query(Servo).filter(Servo.id == servo_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Servo]:
        """Obtener Servo por nombre"""
        return db.query(Servo).filter(Servo.name == name).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Servo]:
        """Obtener todos los Servos con paginación"""
        return db.query(Servo).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, servo_id: int, servo: ServoUpdate) -> Optional[Servo]:
        """Actualizar un Servo"""
        db_servo = db.query(Servo).filter(Servo.id == servo_id).first()
        if not db_servo:
            return None
        
        # Actualizar solo los campos que tienen valor
        update_data = servo.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servo, key, value)
        
        db.add(db_servo)
        db.commit()
        db.refresh(db_servo)
        return db_servo
    
    @staticmethod
    def delete(db: Session, servo_id: int) -> bool:
        """Eliminar un Servo"""
        db_servo = db.query(Servo).filter(Servo.id == servo_id).first()
        if not db_servo:
            return False
        
        db.delete(db_servo)
        db.commit()
        return True
    
    @staticmethod
    def get_active(db: Session) -> List[Servo]:
        """Obtener todos los Servos activos"""
        return db.query(Servo).filter(Servo.is_active == True).all()
