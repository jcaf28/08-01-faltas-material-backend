# app/schemas/kit.py

from pydantic import BaseModel
from typing import Optional, List

class KitBase(BaseModel):
    id_kit: str
    id_vertice: str
    edicion: int
    cantidad: int
    va_a_linea: Optional[bool] = False

class KitCreate(KitBase):
    pass

class KitInDBBase(KitBase):
    class Config:
        orm_mode = True

class Kit(KitInDBBase):
    pass
