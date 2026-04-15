from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from typing import List

from settings import device_mapping


def convert_attr_to_options(class_obj):
    """Convierte los atributos de una clase a un esquema de opciones"""
    options = {}
    for attr_name in dir(class_obj):
        print(f"Revisando atributo: {attr_name}")
        attr = getattr(class_obj, attr_name)
        print(f"  Atributo: {attr_name}, es callable: {callable(attr)}, tiene is_option: {hasattr(attr, 'is_option')}")
        if callable(attr) and hasattr(attr, "is_option"):
            print(f"  → Atributo '{attr_name}' es una opción válida")
            options[attr_name] = {
                "type": attr.option_type,
                "description": attr.option_description
            }
    print(f"Opciones convertidas para {class_obj.__name__}: {options}")
    return options

ruter = APIRouter(prefix="/devices", tags=["devices"])

@ruter.get("/", response_model=List[str])
def list_devices():
    """Listar todos los dispositivos disponibles"""
    return list(device_mapping.keys())