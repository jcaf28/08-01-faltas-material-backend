# app/api/routers/admin.py

from fastapi import APIRouter, HTTPException
from app.services.etl.importar_excel_kits import importar_excel_kits

router_admin = APIRouter()

@router_admin.post("/importar_kits")
async def importar_kits():
    try:
        await importar_excel_kits()
        return {"message": "La importación de kits ha sido realizada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))