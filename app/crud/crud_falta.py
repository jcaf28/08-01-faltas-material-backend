# app/crud/crud_falta.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import falta as falta_schema
from typing import List

def create_falta(db: Session, falta: falta_schema.FaltaCreate):
    db_falta = models.Falta(**falta.model_dump())
    db.add(db_falta)
    db.commit()
    db.refresh(db_falta)
    return db_falta

def get_faltas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Falta).order_by(models.Falta.timestamp.desc()).offset(skip).limit(limit).all()

def get_faltas_by_matricula_bogie(db: Session, matricula_bogie: str, skip: int = 0, limit: int = 10) -> List[models.Falta]:
    return (
        db.query(models.Falta)
        .filter(models.Falta.matricula_bogie == matricula_bogie)
        .order_by(models.Falta.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )