# app/main.py

# main.py

from fastapi import FastAPI
from .api.routers import admin

app = FastAPI()
app.title = "CAF Div3 Acabados - Gestión de Faltas"
app.version = "0.1"

app.include_router(admin.router)