# app/crud/crud_kit.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import kit as kit_schema

def get_kit(db: Session, id_kit: str):
    return db.query(models.Kit).filter(models.Kit.id_kit == id_kit).first()

def get_kits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kit).order_by(models.Kit.id_kit).offset(skip).limit(limit).all()

def get_kits_by_vertice(db: Session, id_vertice: str, skip: int = 0, limit: int = 100):
    return db.query(models.Kit).filter(models.Kit.id_vertice == id_vertice).order_by(models.Kit.id_kit).offset(skip).limit(limit).all()
