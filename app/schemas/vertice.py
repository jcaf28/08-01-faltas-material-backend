# app/schemas/vertice.py

from typing import List, Optional
from pydantic import BaseModel

class VerticeBase(BaseModel):
    id_vertice: str
    id_proyecto: str

class VerticeCreate(VerticeBase):
    pass

class VerticeInDBBase(VerticeBase):
    class Config:
        orm_mode = True

class Vertice(VerticeInDBBase):
    pass
