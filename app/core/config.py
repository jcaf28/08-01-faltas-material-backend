# app/core/config.py

from pydantic import BaseSettings, Field
import os

class Settings(BaseSettings):
    ENTORNO: str = Field(default="desarrollo", env="ENTORNO")
    DEV_DATABASE_SERVER: str = Field(..., env="DEV_DATABASE_SERVER")
    DEV_DATABASE_NAME: str = Field(..., env="DEV_DATABASE_NAME")
    DEV_DATABASE_DRIVER: str = Field(..., env="DEV_DATABASE_DRIVER")

    @property
    def DATABASE_URL(self):
        if self.ENTORNO == "desarrollo":
            return f"mssql+pyodbc://{self.DEV_DATABASE_SERVER}/{self.DEV_DATABASE_NAME}?driver={self.DEV_DATABASE_DRIVER}&TrustServerCertificate=yes"
        elif self.ENTORNO == "produccion":
            pass  # Aquí puedes añadir la lógica para producción
        else:
            raise ValueError("ENTORNO no está configurado correctamente")

    class Config:
        env_file = ".env"

settings = Settings()
