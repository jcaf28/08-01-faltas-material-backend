# app/api/routers/kit.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db

router_kit = APIRouter()

@router_kit.get("/kits/", response_model=List[schemas.Kit])
def read_kits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kits = crud.get_kits(db, skip=skip, limit=limit)
    return kits

@router_kit.get("/kits/{id_kit}", response_model=schemas.Kit)
def read_kit(id_kit: str, db: Session = Depends(get_db)):
    db_kit = crud.get_kit(db, id_kit=id_kit)
    if db_kit is None:
        raise HTTPException(status_code=404, detail="Kit no encontrado")
    return db_kit

@router_kit.get("/vertices/{id_vertice}/kits/", response_model=List[schemas.Kit])
def read_kits_by_vertice(id_vertice: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kits = crud.get_kits_by_vertice(db, id_vertice=id_vertice, skip=skip, limit=limit)
    return kits
