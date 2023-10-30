# app/schemas/articulo.py

from pydantic import BaseModel
from typing import Optional

class ArticuloBase(BaseModel):
    id_articulo: str
    descripcion: Optional[str] = None

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloInDBBase(ArticuloBase):
    class Config:
        orm_mode = True

class Articulo(ArticuloInDBBase):
    pass
