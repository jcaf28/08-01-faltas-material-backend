# app/schemas/articulo_kit.py

from pydantic import BaseModel
from typing import Optional

class ArticuloKitBase(BaseModel):
    id_articulo_kit: int
    id_articulo: str
    id_kit: str
    cantidad: int

class ArticuloKitCreate(ArticuloKitBase):
    pass

class ArticuloKitInDBBase(ArticuloKitBase):
    class Config:
        orm_mode = True

class ArticuloKit(ArticuloKitInDBBase):
    pass
