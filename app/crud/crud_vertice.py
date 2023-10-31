# app/crud/crud_vertice.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import vertice as vertice_schema

def get_vertice(db: Session, vertice_id: str):
    return db.query(models.Vertice).filter(models.Vertice.id_vertice == vertice_id).first()

def get_vertices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vertice).order_by(models.Vertice.id_vertice).offset(skip).limit(limit).all()

def get_vertices_by_proyecto(db: Session, proyecto_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Vertice).filter(models.Vertice.id_proyecto == proyecto_id).order_by(models.Vertice.id_vertice).offset(skip).limit(limit).all()
