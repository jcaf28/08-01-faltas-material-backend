# app/api/routers/proyecto.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router_proyecto = APIRouter()

# @router_proyecto.post("/proyectos/", response_model=schemas.Proyecto)
# def create_proyecto(proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
#     db_proyecto = crud.get_proyecto(db, proyecto_id=proyecto.id_proyecto)
#     if db_proyecto:
#         raise HTTPException(status_code=400, detail="Proyecto ya registrado")
#     return crud.create_proyecto(db=db, proyecto=proyecto)

@router_proyecto.get("/proyectos/", response_model=List[schemas.Proyecto])
def read_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyectos = crud.get_proyectos(db, skip=skip, limit=limit)
    return proyectos

@router_proyecto.get("/proyectos/{proyecto_id}", response_model=schemas.Proyecto)
def read_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    db_proyecto = crud.get_proyecto(db, proyecto_id=proyecto_id)
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto
