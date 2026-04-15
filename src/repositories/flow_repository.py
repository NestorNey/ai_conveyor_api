from sqlalchemy.orm import Session
from src.models import FlowPresetModel
from src.schemas import FlowPresetSchema, FlowPresetUpdate  # El que creamos antes
from typing import Optional, List
from sqlalchemy.orm.attributes import flag_modified

class FlowPresetRepository:
    """Repositorio para operaciones CRUD de Presets de Flows"""
    
    @staticmethod
    def create(db: Session, preset: FlowPresetSchema) -> FlowPresetModel:
        """Guardar un nuevo preset (el chorisote de opciones)"""
        db_preset = FlowPresetModel(
            name=preset.name,
            flow_name=preset.flow_name,
            options=preset.options,
            is_default=preset.is_default
        )
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        return db_preset

    @staticmethod
    def get_by_flow(db: Session, flow_name: str) -> List[FlowPresetModel]:
        """Obtener todos los presets de un flow específico (ej: blue_component_detection)"""
        return db.query(FlowPresetModel).filter(
            FlowPresetModel.flow_name == flow_name
        ).all()

    @staticmethod
    def get_default_by_flow(db: Session, flow_name: str) -> Optional[FlowPresetModel]:
        """Obtener el preset marcado como default para un flow"""
        return db.query(FlowPresetModel).filter(
            FlowPresetModel.flow_name == flow_name,
            FlowPresetModel.is_default == True
        ).first()

    @staticmethod
    def delete(db: Session, preset_id: int) -> bool:
        """Eliminar un preset por ID"""
        db_preset = db.query(FlowPresetModel).filter(FlowPresetModel.id == preset_id).first()
        if not db_preset:
            return False
        
        db.delete(db_preset)
        db.commit()
        return True

    @staticmethod
    def update_options(db: Session, preset_id: int, new_options: dict):
        db_preset = db.query(FlowPresetModel).filter(FlowPresetModel.id == preset_id).first()
        if db_preset:
            setattr(db_preset, "options", new_options) # Asegura que SQLAlchemy vea el cambio
            flag_modified(db_preset, "options") # Asegura que SQLAlchemy vea el cambio
            db.commit()
            db.refresh(db_preset)
        return db_preset