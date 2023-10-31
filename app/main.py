# app/main.py

# main.py

from fastapi import FastAPI
from api.routers import admin
from middlewares.error_handler import ErrorHandlerMiddleware

app = FastAPI()
app.title = "CAF Div3 Acabados - Gestión de Faltas"
app.version = "0.1"

# Registra el middleware
app.add_middleware(ErrorHandlerMiddleware)

# Registra las rutas
app.include_router(admin.router_admin, prefix="/admin", tags=["admin"])