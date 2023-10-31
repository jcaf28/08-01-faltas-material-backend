# app/main.py

from fastapi import FastAPI
from .api.routers import admin, proyecto
from .middlewares.error_handler import ErrorHandlerMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "CAF Div3 Acabados - Gestión de Faltas"
app.version = "0.1"

# Registra el middleware
# app.add_middleware(ErrorHandlerMiddleware)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Permite todos los orígenes
#     allow_credentials=True,
#     allow_methods=["*"],  # Permite todos los métodos
#     allow_headers=["*"],  # Permite todos los headers
# )

# Registra las rutas
app.include_router(admin.router_admin, prefix="/admin", tags=["admin"])
app.include_router(proyecto.router_proyecto, prefix="/proyectos", tags=["proyectos"])