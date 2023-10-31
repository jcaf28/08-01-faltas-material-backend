# app/crud/crud_bogie.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import bogie as bogie_schema

def get_bogie(db: Session, matricula: str):
    return db.query(models.Bogie).filter(models.Bogie.matricula == matricula).first()

def get_bogies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bogie).order_by(models.Bogie.matricula).offset(skip).limit(limit).all()

def get_bogies_by_vertice(db: Session, id_vertice: str, skip: int = 0, limit: int = 100):
    return db.query(models.Bogie).filter(models.Bogie.id_vertice == id_vertice).order_by(models.Bogie.matricula).offset(skip).limit(limit).all()
