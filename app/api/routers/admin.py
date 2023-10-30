# app/api/routers/admin.py

from fastapi import APIRouter, HTTPException
from app.services.db import clean_db
from app.services.etl import importar_excel_kits

router = APIRouter(prefix="/admin")

@router.post("/limpiar_bd")
async def limpiar_base_de_datos():
    try:
        clean_db.limpiar_bd()
        return {"message": "La base de datos ha sido limpiada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/importar_kits")
async def importar_kits():
    try:
        importar_excel_kits.ejecutar_importacion()
        return {"message": "La importación de kits ha sido realizada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))