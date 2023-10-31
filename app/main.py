# app/main.py

from fastapi import FastAPI
from .api.routers import admin, proyecto, vertice, bogie, kit, articulo, articulo_kit
from .middlewares.error_handler import ErrorHandlerMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "CAF Div3 Acabados - Gestión de Faltas"
app.version = "0.1"

# Registra el middleware
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Registra las rutas
app.include_router(admin.router_admin, prefix="/admin", tags=["admin"])
app.include_router(proyecto.router_proyecto, prefix="/proyectos", tags=["proyectos"])
app.include_router(vertice.router_vertice, prefix="/api", tags=["vertice"])
app.include_router(bogie.router_bogie, prefix="/api/v1", tags=["bogies"])
app.include_router(kit.router_kit, prefix="/api/v1", tags=["kits"])
app.include_router(articulo.router_articulo, prefix="/api/v1", tags=["articulos"])
app.include_router(articulo_kit.router, prefix="/api/v1", tags=["articulo_kit"])

