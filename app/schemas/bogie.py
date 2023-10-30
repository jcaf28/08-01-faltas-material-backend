# app/schemas/bogie.py

from pydantic import BaseModel
from typing import Optional

class BogieBase(BaseModel):
    matricula: str
    id_vertice: str

class BogieCreate(BogieBase):
    pass

class BogieInDBBase(BogieBase):
    class Config:
        orm_mode = True

class Bogie(BogieInDBBase):
    pass
