# app/services/etl/_funciones_auxiliares.py

# _funciones_auxiliares.py

import sys
sys.path.append('.')

import os
import io
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables del archivo .env
ENTORNO = os.getenv('ENTORNO') 


######### FUNCIONES AUXILIARES ############

def listar_excels_en_carpeta(carpeta):
    archivos = os.listdir(carpeta)
    archivos_excel = [archivo for archivo in archivos if archivo.endswith(".xlsx")]
    return [os.path.join(carpeta, archivo) for archivo in archivos_excel]

def escribir_log(mensaje, ruta_logs, nombre_log):
    with io.open(os.path.join(ruta_logs, nombre_log), 'a', encoding='utf-8') as log_file:
        log_file.write(mensaje + "\n")

def nombre_archivo_log():
    if ENTORNO == 'desarrollo':
        return "log_errores.txt"
    else:
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        return f"log_errores_{timestamp}.txt"
    
def buscar_archivo_bogies_entregados(carpeta_bast):
    # 1. Obtener las claves y las obras del Excel en carpeta_bast
    archivos_excel = [f for f in os.listdir(carpeta_bast) if f.startswith('BOGIES_ENTREGADOS_') and f.endswith('.xlsx')]
    
    # Ordenar por fecha de modificación y tomar el más reciente
    archivo_reciente = max(archivos_excel, key=lambda x: os.path.getmtime(os.path.join(carpeta_bast, x)))
    
    return archivo_reciente

def obtener_proyectos(carpeta_bast, ruta_archivos):
    
    archivo_reciente = buscar_archivo_bogies_entregados(carpeta_bast)
    ruta_archivo_reciente = os.path.join(carpeta_bast, archivo_reciente)
    
    df = pd.read_excel(ruta_archivo_reciente, sheet_name="0.INDICE", skiprows=2, engine="openpyxl")
    
    dict_clave_obra = dict(zip(df["CLAVE"], df["OBRA"]))
    
    # 2. Identificar las subcarpetas en ruta_archivos que comienzan con una clave
    for clave in dict_clave_obra.keys():
        str_clave = str(clave)  # Convertir clave a cadena
        subcarpetas = [d for d in os.listdir(ruta_archivos) if os.path.isdir(os.path.join(ruta_archivos, d)) and d.startswith(str_clave)]
        for subcarpeta in subcarpetas:
            ruta_subcarpeta = os.path.join(ruta_archivos, subcarpeta)
            archivos_subcarpeta = [f for f in os.listdir(ruta_subcarpeta) if f.startswith(str(clave)) and f.endswith(('.xlsx'))]

            
            # Si hay archivos que coinciden, tomar el más reciente y añadir su ruta al diccionario
            if archivos_subcarpeta:
                archivo_reciente_subcarpeta = max(archivos_subcarpeta, key=lambda x: os.path.getmtime(os.path.join(ruta_subcarpeta, x)))
                dict_clave_obra[clave] = {
                    "OBRA": dict_clave_obra[clave],
                    "EXCEL KITS": os.path.join(ruta_subcarpeta, archivo_reciente_subcarpeta)
                }
    
    return dict_clave_obra

def buscar_hoja_por_key(archivo, key):
    """Busca en el archivo Excel una hoja que comience con el key proporcionado. Retorna el nombre de la hoja si la encuentra."""
    with pd.ExcelFile(archivo, engine="openpyxl") as xls:
        for sheet_name in xls.sheet_names:
            if sheet_name.startswith(str(key)):
                return sheet_name
    return None
    
