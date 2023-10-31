# app/api/routers/vertice.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router_vertice = APIRouter()

@router_vertice.get("/vertices/", response_model=List[schemas.Vertice])
def read_vertices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vertices = crud.get_vertices(db, skip=skip, limit=limit)
    return vertices

@router_vertice.get("/vertices/{vertice_id}", response_model=schemas.Vertice)
def read_vertice(vertice_id: str, db: Session = Depends(get_db)):
    db_vertice = crud.get_vertice(db, vertice_id=vertice_id)
    if db_vertice is None:
        raise HTTPException(status_code=404, detail="Vértice no encontrado")
    return db_vertice

@router_vertice.get("/proyectos/{proyecto_id}/vertices/", response_model=List[schemas.Vertice])
def read_vertices_by_proyecto(proyecto_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vertices = crud.get_vertices_by_proyecto(db, proyecto_id=proyecto_id, skip=skip, limit=limit)
    return vertices