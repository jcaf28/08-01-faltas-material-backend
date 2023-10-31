# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.ENTORNO = os.getenv("ENTORNO", "desarrollo")

        if self.ENTORNO == 'desarrollo':
            self.server_name = os.getenv("DEV_DATABASE_SERVER")
            self.database_name = os.getenv("DEV_DATABASE_NAME")
            self.driver = os.getenv("DEV_DATABASE_DRIVER")
            self.RUTA_ARCHIVOS = os.getenv('DEV_RUTA_ARCHIVOS')
            self.RUTA_BOGIES_ENTREGADOS = os.getenv('DEV_RUTA_BOGIES_ENTREGADOS')
        elif self.ENTORNO == 'produccion':
            pass
        else:
            raise ValueError("ENTORNO no está configurado correctamente en .env")

    def get_connection_string(self):
        return f"mssql+pyodbc://{self.server_name}/{self.database_name}?driver={self.driver}&TrustServerCertificate=yes"
