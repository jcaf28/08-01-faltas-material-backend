# app/services/etl/importar_excel_kits.py

import sys
sys.path.append('.')

import os
import openpyxl
import asyncio
from concurrent.futures import ProcessPoolExecutor
from ._importar_excel_kits import *
from ._funciones_auxiliares import *
from app.db.session import database_session
from ._funciones_log import escribir_encabezados, escribir_separadores
from app.core.config import Config

from dotenv import load_dotenv
config = Config()

load_dotenv()  # Cargar las variables del archivo .env

ruta_logs = "app/services/etl/logs"
nombre_log = nombre_archivo_log()

ruta_archivos = config.RUTA_ARCHIVOS
ruta_bogies_entregados = config.RUTA_BOGIES_ENTREGADOS
entorno = config.ENTORNO

# Si estamos en modo desarrollo, borramos el log existente (si existe) y generaremos uno nuevo
if ENTORNO == 'desarrollo':
    log_errores = os.path.join(ruta_logs, "log_errores.txt")
    if os.path.exists(log_errores):
        os.remove(log_errores)

    log_resumen = os.path.join(ruta_logs, "log_resumen.txt")
    if os.path.exists(log_resumen):
        os.remove(log_resumen)

if ENTORNO == 'produccion':
    nombre_log = nombre_archivo_log()  # Obtener el nombre del archivo de log con timestamp
    log_path = os.path.join(ruta_logs, nombre_log)

proyectos = obtener_proyectos(ruta_bogies_entregados, ruta_archivos)

def importar_datos_proyecto(key, proyecto, log_errores, log_resumen, ruta_bogies_entregados):

    with database_session as db:
        # Importar datos Proyectos
        importar_proyecto(key, proyecto, db, log_errores, log_resumen)
        # Buscar y leer datos vértices y bogies
        importar_datos_bogies_entregados(key, ruta_bogies_entregados, db, log_resumen, log_errores)
        # Importar datos kits
        importar_datos_kits(key, proyecto, db, log_errores, log_resumen)

def importar_datos_bogies_entregados(key, ruta_bogies_entregados, db, log_resumen, log_errores):
    archivo = buscar_archivo_bogies_entregados(ruta_bogies_entregados)
    nombre_archivo = os.path.basename(archivo)
    ruta_archivo = os.path.join(ruta_bogies_entregados, nombre_archivo)

    sheet_name = buscar_hoja_por_key(ruta_archivo, key)
    
    if not sheet_name:
        raise Exception(f"No se encontró una hoja que comience con {key} en el archivo.")
    
    df = pd.read_excel(ruta_archivo, sheet_name=sheet_name, skiprows=5, engine="openpyxl")
    
    importar_vertices(key, df, db, log_resumen, log_errores)
    importar_bogies(key,df,db, log_resumen, log_errores)

def importar_datos_kits(key, proyecto, db, log_resumen, log_errores):
    ruta_excel = proyecto['EXCEL KITS']
    workbook = openpyxl.load_workbook(ruta_excel, data_only=True)  # Cargar con valores calculados
    sheet = workbook[workbook.sheetnames[0]]

    importar_kits(key, sheet, db, log_resumen, log_errores)
    importar_articulos(sheet, db, log_resumen, log_errores)
    importar_articulos_por_kit(sheet, db, log_resumen, log_errores)

async def importar_excel_kits():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        for key, proyecto in proyectos.items():
            if isinstance(proyecto, dict) and 'OBRA' in proyecto and 'EXCEL KITS' in proyecto:
                escribir_encabezados(proyecto['OBRA'], log_errores, log_resumen)
                await loop.run_in_executor(executor, importar_datos_proyecto, key, proyecto, log_errores, log_resumen, ruta_bogies_entregados)
                escribir_separadores(log_errores, log_resumen)

        print("Importación finalizada.")