# app/crud/crud_proyecto.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import proyecto as proyecto_schema

def get_proyecto(db: Session, proyecto_id: str):
    return db.query(models.Proyecto).filter(models.Proyecto.id_proyecto == proyecto_id).first()

def get_proyectos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proyecto).order_by(models.Proyecto.id_proyecto).offset(skip).limit(limit).all()

