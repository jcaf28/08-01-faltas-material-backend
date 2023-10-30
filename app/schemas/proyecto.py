# app/schemas/proyecto.py

from typing import List, Optional
from pydantic import BaseModel

class ProyectoBase(BaseModel):
    id_proyecto: str
    nombre: Optional[str] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoInDBBase(ProyectoBase):
    class Config:
        orm_mode = True

class Proyecto(ProyectoInDBBase):
    pass
