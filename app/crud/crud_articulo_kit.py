# app/crud/crud_articulo_kit.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import articulo_kit as articulo_kit_schema

def get_articulo_kit(db: Session, id_articulo_kit: int):
    return db.query(models.ArticuloKit).filter(models.ArticuloKit.id_articulo_kit == id_articulo_kit).first()

def get_articulos_kit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ArticuloKit).offset(skip).limit(limit).all()

def get_articulo_kit_by_kit_id(db: Session, kit_id: str):
    return db.query(models.ArticuloKit).filter(models.ArticuloKit.id_kit == kit_id).all()
