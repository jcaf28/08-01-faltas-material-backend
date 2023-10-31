# app/middlewares/error_handler.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Intenta procesar la solicitud y obtener la respuesta
            response = await call_next(request)
        except HTTPException as exc:
            # Captura excepciones de tipo HTTPException y devuelve una respuesta JSON
            return JSONResponse(
                content={"detail": exc.detail},
                status_code=exc.status_code,
            )
        except Exception as exc:
            # Captura cualquier otra excepción y devuelve una respuesta 500
            return JSONResponse(
                content={"detail": "Internal Server Error"},
                status_code=500,
            )
        return response