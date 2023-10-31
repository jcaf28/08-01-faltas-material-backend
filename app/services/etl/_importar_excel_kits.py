# _importar_excel_kits.py

import sys
sys.path.append('.')

import os
from app.models.models import *
from dotenv import load_dotenv
import re
import re

import re

from _funciones_auxiliares import *
from _funciones_log import escribir_resumen

load_dotenv()  # Cargar las variables del archivo .env
ENTORNO = os.getenv('ENTORNO') 


############ FUNCIONES DE IMPORTACIÓN DE DATOS ##################
    

def importar_proyecto(key, proyecto_dict, db, log_errores, log_resumen):

    nombre = proyecto_dict.get('OBRA')
    if not nombre:
        raise ValueError("El campo 'OBRA' no está presente en el diccionario.")

    total_intentos = 0
    total_exitos = 0
    try:
        proyecto_existente = db.query(Proyecto).filter_by(id_proyecto=key).first()
        total_intentos += 1

        if proyecto_existente:
            proyecto_existente.nombre = nombre
            db.add(proyecto_existente)
        else:
            proyecto = Proyecto(id_proyecto=key, nombre=nombre)
            db.add(proyecto)

        db.commit()
        total_exitos += 1

        # Añadir la información al log de resumen
        escribir_resumen(log_resumen, total_intentos, total_exitos, tabla="Proyectos")
        
    except Exception as e:
        with open(log_errores, 'a') as log_file:
            log_file.write(f"Error al insertar/actualizar el proyecto. Error: {str(e)}\n")

def importar_vertices(key, df, db, log_resumen, log_errores):
    total_intentos = 0
    total_exitos = 0
    total_errores = 0

    try:
        if 'VÉRTICE' not in df.columns:
            raise ValueError("La columna 'VÉRTICE' no está presente en el DataFrame.")
        
        vertices_unicos = df['VÉRTICE'].dropna().str.split('-').str[0].unique()
        
        for vertice in vertices_unicos:
            total_intentos += 1
            id_vertice = f"{key}_{vertice}"

            vertice_existente = db.query(Vertice).filter_by(id_vertice=id_vertice).first()

            if not vertice_existente:
                nuevo_vertice = Vertice(id_vertice=id_vertice, id_proyecto=str(key))
                db.add(nuevo_vertice)
            else:
                # Actualiza los valores necesarios del vértice existente
                vertice_existente.id_proyecto = str(key)  # Asumiendo que quieras actualizar este campo
                # Actualiza otros campos según sea necesario
                # db.add(vertice_existente)  # Esto puede ser necesario dependiendo de la configuración de tu ORM

            db.commit()  # Asegúrate de que la transacción se completa correctamente
            total_exitos += 1  # Contabiliza el éxito solo si la transacción es exitosa
        
        escribir_resumen(log_resumen, total_intentos, total_exitos, tabla="Vertices")
        
    except Exception as e:
        total_errores += total_intentos  # Todos los intentos han resultado en error
        error_msg = f"Error al importar vértices para el proyecto {key}: {str(e)}"
        print(error_msg)
        with open(log_errores, 'a', encoding='utf-8') as log_file:
            log_file.write(error_msg + "\n")
        escribir_resumen(log_resumen, total_intentos, total_exitos, tabla="Vertices")

def importar_bogies(key, df, db, log_resumen, log_errores):
    total_intentos = 0
    total_exitos = 0
    total_errores = 0

    try:
        if 'MATRÍCULA' not in df.columns or 'VÉRTICE' not in df.columns:
            raise ValueError("Las columnas necesarias 'MATRÍCULA' o 'VÉRTICE' no están presentes en el DataFrame.")
        
        for _, row in df.dropna(subset=['MATRÍCULA', 'VÉRTICE']).iterrows():
            total_intentos += 1
            matricula = row['MATRÍCULA']
            vertice_parte_izq = row['VÉRTICE'].split('-')[0]
            id_vertice = f"{key}_{vertice_parte_izq}"

            vertice_existente = db.query(Vertice).filter_by(id_vertice=id_vertice).first()

            if not vertice_existente:
                error_msg = f"Vertice {id_vertice} no encontrado en la BD. Ignorando bogie con matricula {matricula}."
                print(error_msg)
                with open(log_errores, 'a', encoding='utf-8') as log_file:
                    log_file.write(error_msg + "\n")
                total_errores += 1
                continue

            bogie_existente = db.query(Bogie).filter_by(matricula=matricula).first()

            if not bogie_existente:
                nuevo_bogie = Bogie(matricula=matricula, id_vertice=id_vertice)
                db.add(nuevo_bogie)
            else:
                actualizado = False
                if bogie_existente.id_vertice != id_vertice:
                    bogie_existente.id_vertice = id_vertice
                    actualizado = True

                # Aquí debes añadir código para actualizar el resto de los campos de bogie_existente según sea necesario
                # ...

                if actualizado:
                    db.add(bogie_existente)

            db.commit()
            total_exitos += 1

        escribir_resumen(log_resumen, total_intentos, total_exitos, tabla="Bogies")

    except Exception as e:
        total_errores += total_intentos - total_exitos
        error_msg = f"Error al importar bogies para el proyecto {key}: {str(e)}"
        print(error_msg)
        with open(log_errores, 'a', encoding='utf-8') as log_file:
            log_file.write(error_msg + "\n")
        escribir_resumen(log_resumen, total_intentos, total_exitos, tabla="Bogies")

def importar_kits(key, sheet, db, log_errores, log_resumen):
    total_intentos = 0
    total_exitos = 0
    errores = 0
    
    # Pasamos key a tipo string
    key = str(key)

    columna_kit = None
    columna_edicion = None
    
    for col_num in range(sheet.max_column):
        cell = sheet.cell(row=1, column=col_num + 1)
        if cell.value == 'KIT':
            columna_kit = col_num
        elif cell.value == 'EDICION':
            columna_edicion = col_num
    
    if columna_kit is None or columna_edicion is None:
        with open(log_errores, 'a', encoding='utf-8') as log_file:
            log_file.write("Error general: No se encontraron las columnas necesarias ('KIT' y 'EDICION')\n")
        escribir_resumen(log_resumen, total_intentos, total_exitos, 'Kits')
        return
    
    for row_num in range(2, sheet.max_row + 1):
        kit_cell = sheet.cell(row=row_num, column=columna_kit + 1)
        edicion_cell = sheet.cell(row=row_num, column=columna_edicion + 1)
        
        if kit_cell.value is None and edicion_cell.value is None:
            break

        total_intentos += 1
        
        kit_value = str(kit_cell.value).strip() if kit_cell.value is not None else None
        edicion_value = str(edicion_cell.value).strip() if edicion_cell.value is not None else None
        
        if kit_value is None:
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Fila {row_num}: La celda de la columna 'KIT' está vacía.\n")
            errores += 1
            continue
        
        match = re.match(r'(\d+)?([A-Z0-9.]+)-([A-Z])(\d*)?@?', kit_value)

        if not match:
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Error en 'KIT': Valor no válido o no coincide con el key: {kit_value}\n")
            errores += 1
            continue
        
        id_vertice = f"{key}_{match.group(3)}"
        cantidad = int(match.group(4)) if match.group(4) else 1
        va_a_linea = bool(match.group(0).endswith('@'))
        
        try:
            edicion = int(edicion_value)
        except ValueError:
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Error en 'EDICION': Valor no es un número entero: {edicion_value}\n")
            errores += 1
            continue
        
        kit_existente = db.query(Kit).filter_by(id_kit=kit_value).first()
        
        if not kit_existente:
            nuevo_kit = Kit(id_kit=kit_value, id_vertice=id_vertice, edicion=edicion, cantidad=cantidad, va_a_linea=va_a_linea)
            db.add(nuevo_kit)
        else:
            kit_existente.id_vertice = id_vertice
            kit_existente.edicion = edicion
            kit_existente.cantidad = cantidad
            kit_existente.va_a_linea = va_a_linea
            db.add(kit_existente)
            
        try:
            db.commit()
            total_exitos += 1
        except Exception as e:
            db.rollback()
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Error al intentar añadir/actualizar el kit en la base de datos: {str(e)}\n")
            errores += 1
    
    escribir_resumen(log_resumen, total_intentos, total_exitos, 'Kits')

def importar_articulos(sheet, db, log_errores, log_resumen):
    total_intentos = 0
    total_exitos = 0
    errores = 0
    
    columna_articulo = None
    columna_descripcion = None
    
    for col_num in range(sheet.max_column):
        cell = sheet.cell(row=1, column=col_num + 1)
        if cell.value == 'ARTICULO':
            columna_articulo = col_num
        elif cell.value == 'DESCRIPCIÓN CÓDIGO':
            columna_descripcion = col_num
    
    if columna_articulo is None:
        with open(log_errores, 'a', encoding='utf-8') as log_file:
            log_file.write("Error general: No se encontró la columna necesaria 'ARTICULO'\n")
        escribir_resumen(log_resumen, total_intentos, total_exitos, 'Articulos')
        return
    
    for row_num in range(2, sheet.max_row + 1):
        articulo_cell = sheet.cell(row=row_num, column=columna_articulo + 1)
        descripcion_cell = sheet.cell(row=row_num, column=columna_descripcion + 1) if columna_descripcion is not None else None
        
        if articulo_cell.value is None:
            break

        total_intentos += 1
        
        id_articulo = str(articulo_cell.value).strip() if articulo_cell.value != "#N/A" else None
        descripcion = str(descripcion_cell.value).strip() if descripcion_cell and descripcion_cell.value not in [None, "#N/A"] else None
        
        if not id_articulo:
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Fila {row_num}: La celda de la columna 'ARTICULO' está vacía, solo contiene espacios o contiene '#N/A'.\n")
            errores += 1
            continue
        
        articulo_existente = db.query(Articulo).filter_by(id_articulo=id_articulo).first()
        
        if not articulo_existente:
            nuevo_articulo = Articulo(id_articulo=id_articulo, descripcion=descripcion)
            db.add(nuevo_articulo)
        else:
            if columna_descripcion is not None:
                articulo_existente.descripcion = descripcion
                db.add(articulo_existente)
            else:
                # Si no existe la columna 'DESCRIPCIÓN CÓDIGO', se respeta la descripción existente en la BD
                total_exitos += 1
                continue
            
        try:
            db.commit()
            total_exitos += 1
        except Exception as e:
            db.rollback()
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Error al intentar añadir/actualizar el artículo en la base de datos: {str(e)}\n")
            errores += 1
    
    escribir_resumen(log_resumen, total_intentos, total_exitos, 'Articulos')

def importar_articulos_por_kit(sheet, db, log_errores, log_resumen):
    total_intentos = 0
    total_exitos = 0
    errores = 0

    columna_articulo = None
    columna_kit = None
    columna_cantidad = None

    for col_num in range(sheet.max_column):
        cell = sheet.cell(row=1, column=col_num + 1)
        if cell.value == 'ARTICULO':
            columna_articulo = col_num
        elif cell.value == 'KIT':
            columna_kit = col_num
        elif cell.value == 'CANTIDAD':
            columna_cantidad = col_num

    if columna_articulo is None or columna_kit is None:
        with open(log_errores, 'a', encoding='utf-8') as log_file:
            log_file.write("Error general: No se encontraron las columnas necesarias 'ARTICULO' o 'KIT'\n")
        escribir_resumen(log_resumen, total_intentos, total_exitos, 'Articulos por Kit')
        return

    kits_articulos = {}

    for row_num in range(2, sheet.max_row + 1):
        total_intentos += 1
        try:
            id_articulo_cell = sheet.cell(row=row_num, column=columna_articulo + 1)
            id_kit_cell = sheet.cell(row=row_num, column=columna_kit + 1)
            cantidad_cell = sheet.cell(row=row_num, column=columna_cantidad + 1) if columna_cantidad is not None else None

            if id_articulo_cell.value is None or id_kit_cell.value is None:
                continue

            id_articulo = str(id_articulo_cell.value).strip() if id_articulo_cell.value != "#N/A" else None
            id_kit = str(id_kit_cell.value).strip() if id_kit_cell.value != "#N/A" else None

            cantidad_raw = cantidad_cell.value if cantidad_cell else 1
            if isinstance(cantidad_raw, int):
                cantidad = cantidad_raw
            elif cantidad_raw not in [None, "#N/A"]:
                try:
                    cantidad = int(cantidad_raw)
                except ValueError:
                    cantidad = 0
            else:
                cantidad = 0

            if not id_articulo or not id_kit or cantidad <= 0:
                with open(log_errores, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"Fila {row_num}: Datos inválidos. ARTICULO: {id_articulo}, KIT: {id_kit}, CANTIDAD: {cantidad}\n")
                errores += 1
                continue

            if (id_kit, id_articulo) not in kits_articulos:
                kits_articulos[(id_kit, id_articulo)] = cantidad
            else:
                kits_articulos[(id_kit, id_articulo)] += cantidad

        except Exception as e:
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Fila {row_num}: Error al procesar la fila: {str(e)}\n")
            errores += 1

    for (id_kit, id_articulo), cantidad in kits_articulos.items():
        try:
            kit = db.query(Kit).filter_by(id_kit=id_kit).first()
            articulo = db.query(Articulo).filter_by(id_articulo=id_articulo).first()

            if not kit or not articulo:
                with open(log_errores, 'a', encoding='utf-8') as log_file:
                    if not kit:
                        log_file.write(f"No se encontró el kit con ID {id_kit}\n")
                    if not articulo:
                        log_file.write(f"No se encontró el artículo con ID {id_articulo}\n")
                errores += 1
                continue

            articulo_kit = db.query(ArticuloKit).filter_by(id_kit=id_kit, id_articulo=id_articulo).first()

            if articulo_kit is None:
                nuevo_articulo_kit = ArticuloKit(id_articulo=id_articulo, id_kit=id_kit, cantidad=cantidad * kit.cantidad)
                db.add(nuevo_articulo_kit)
            else:
                articulo_kit.cantidad = cantidad * kit.cantidad
                db.add(articulo_kit)

            db.commit()
            total_exitos += 1

        except Exception as e:
            db.rollback()
            with open(log_errores, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Error al intentar añadir/actualizar el artículo en la base de datos: {str(e)}\n")
            errores += 1

    escribir_resumen(log_resumen, total_intentos, total_exitos, 'Articulos por Kit')


