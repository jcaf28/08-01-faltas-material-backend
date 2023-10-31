# app/api/routers/articulo_kit.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router = APIRouter()

@router.get("/articulos_kit/", response_model=List[schemas.ArticuloKit])
def read_articulos_kit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_articulos_kit(db, skip=skip, limit=limit)

@router.get("/articulos_kit/id_articulokit/{id_articulo_kit}", response_model=List[schemas.ArticuloKit])
def read_articulo_kit_by_articulo_kit_id(id_articulo_kit: int, db: Session = Depends(get_db)):
    result = crud.get_articulo_kit(db, id_articulo_kit=id_articulo_kit)
    if result is None or not result:
        raise HTTPException(status_code=404, detail="ArticuloKit no encontrado")
    return result

@router.get("/articulos_kit/kit/{id_kit}", response_model=List[schemas.ArticuloKit])
def read_articulo_kit_by_kit_id(id_kit: str, db: Session = Depends(get_db)):
    return crud.get_articulo_kit_by_kit_id(db, id_kit=id_kit)