# # app/api/routers/admin.py

# from fastapi import APIRouter, HTTPException

# router_faltas = APIRouter()

# @router_faltas.get("/proyectos", response_model=List[schemas.Proyecto])
# def leer_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     proyectos = crud.get_proyectos(db, skip=skip, limit=limit)
#     return proyectos