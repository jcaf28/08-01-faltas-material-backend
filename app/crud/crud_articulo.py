# app/crud/crud_articulo.py

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import articulo as articulo_schema

def get_articulo(db: Session, id_articulo: str):
    return db.query(models.Articulo).filter(models.Articulo.id_articulo == id_articulo).first()

def get_articulos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Articulo).order_by(models.Articulo.id_articulo).offset(skip).limit(limit).all()

def get_articulos_by_kit(db: Session, id_kit: str, skip: int = 0, limit: int = 100):
    return db.query(models.Articulo).join(models.ArticuloKit).filter(models.ArticuloKit.id_kit == id_kit).order_by(models.Articulo.id_articulo).offset(skip).limit(limit).all()
