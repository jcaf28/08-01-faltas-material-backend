# app/services/etl/_funciones_log.py

# _funciones_log.py

def escribir_encabezados(nombre_proyecto, log_errores, log_resumen):
    with open(log_errores, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n############# {nombre_proyecto} ##################\n")
    with open(log_resumen, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n############# {nombre_proyecto} ##################\n")

def escribir_separadores(log_errores, log_resumen):
    with open(log_errores, 'a', encoding='utf-8') as log_file:
        log_file.write("\n####################################################\n")
    with open(log_resumen, 'a', encoding='utf-8') as log_file:
        log_file.write("\n####################################################\n")

def escribir_resumen(log_resumen, total_intentos, total_exitos, tabla):
    with open(log_resumen, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n*** Tabla '{tabla}' ***:\n")
            log_file.write(f"Intentos: {total_intentos}\n")
            log_file.write(f"Éxitos: {total_exitos}\n")
            log_file.write(f"Errores: {total_intentos-total_exitos}\n")
