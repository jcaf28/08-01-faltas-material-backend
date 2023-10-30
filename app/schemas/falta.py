# app/schemas/falta.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FaltaBase(BaseModel):
    matricula_bogie: str
    id_articulo_kit: int
    cantidad_faltante: int

class FaltaCreate(FaltaBase):
    pass

class FaltaInDBBase(FaltaBase):
    timestamp: datetime

    class Config:
        orm_mode = True

class Falta(FaltaInDBBase):
    pass
