from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import Dict, Type
from josneslib import ClassLoader, FlowRunner

import os

# Configuración de base de datos SQLite
# La BD se crea en la raíz del proyecto
DATABASE_URL = "sqlite:///./ai_conveyor.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

in_memory_db: ClassLoader = ClassLoader(database={}, path="/app/flows")
flow_running: FlowRunner | None = None