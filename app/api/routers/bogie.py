# app/api/routers/bogie.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router_bogie = APIRouter()

@router_bogie.get("/bogies/", response_model=List[schemas.Bogie])
def read_bogies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bogies = crud.get_bogies(db, skip=skip, limit=limit)
    return bogies

@router_bogie.get("/bogies/{matricula}", response_model=schemas.Bogie)
def read_bogie(matricula: str, db: Session = Depends(get_db)):
    db_bogie = crud.get_bogie(db, matricula=matricula)
    if db_bogie is None:
        raise HTTPException(status_code=404, detail="Bogie no encontrado")
    return db_bogie

@router_bogie.get("/vertices/{id_vertice}/bogies/", response_model=List[schemas.Bogie])
def read_bogies_by_vertice(id_vertice: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bogies = crud.get_bogies_by_vertice(db, id_vertice=id_vertice, skip=skip, limit=limit)
    return bogies
