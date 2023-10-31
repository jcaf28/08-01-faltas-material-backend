# app/api/routers/falta.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.db.session import get_db
from typing import Any

router = APIRouter()

@router.post("/faltas/", response_model=schemas.Falta)
def create_falta(
    *,
    db: Session = Depends(get_db),
    falta_in: schemas.FaltaCreate
) -> Any:
    """
    Create new falta.
    """
    falta = crud.create_falta(db=db, falta=falta_in)
    return falta

@router.get("/faltas/", response_model=List[schemas.Falta])
def read_faltas(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve faltas.
    """
    faltas = crud.get_faltas(db, skip=skip, limit=limit)
    return faltas

@router.get("/faltas/{matricula_bogie}", response_model=List[schemas.Falta])
def read_faltas_by_matricula_bogie(
    matricula_bogie: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a list of faltas by matricula bogie.
    """
    faltas = crud.get_faltas_by_matricula_bogie(db, matricula_bogie=matricula_bogie, skip=skip, limit=limit)
    return faltas