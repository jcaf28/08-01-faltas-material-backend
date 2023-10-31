# app/api/routers/articulo.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router_articulo = APIRouter()

@router_articulo.get("/articulos/", response_model=List[schemas.Articulo])
def read_articulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articulos = crud.get_articulos(db, skip=skip, limit=limit)
    return articulos

@router_articulo.get("/articulos/{id_articulo}", response_model=schemas.Articulo)
def read_articulo(id_articulo: str, db: Session = Depends(get_db)):
    db_articulo = crud.get_articulo(db, id_articulo=id_articulo)
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return db_articulo

@router_articulo.get("/kits/{id_kit}/articulos/", response_model=List[schemas.Articulo])
def read_articulos_by_kit(id_kit: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articulos = crud.get_articulos_by_kit(db, id_kit=id_kit, skip=skip, limit=limit)
    return articulos
