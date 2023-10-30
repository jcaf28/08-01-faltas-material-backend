# tools/tree.py

import os
import pyperclip

def list_files(startpath, exclude_dirs):
    def add_directory_structure(structure, root, level):
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else './\n'
        structure += indent + os.path.basename(root) + '/\n'
        return structure

    def add_file_structure(structure, file, level):
        indent = '│   ' * level + '├── '
        structure += indent + file + '\n'
        return structure

    structure = ""
    for root, dirs, files in os.walk(startpath):
        if any(exclude_dir in root for exclude_dir in exclude_dirs):
            continue

        level = root.replace(startpath, '').count(os.sep)
        structure = add_directory_structure(structure, root, level)

        sublevel = level + 1
        for f in sorted(files):
            structure = add_file_structure(structure, f, sublevel)
    return structure

# Modifica esto para incluir las carpetas que quieras excluir
exclude_dirs = ["venv", ".git", "archivos", "__pycache__", ".vscode", "tools"]

try:
    output_dir = "tools"
    os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta tools si no existe
    output_path = os.path.join(output_dir, 'estructura.txt')
    
    # Escribe la estructura del directorio en el archivo 'tools/estructura.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        structure = list_files('.', exclude_dirs)  # Genera la estructura del directorio
        f.write(structure)

    # Copia la estructura del directorio al portapapeles
    pyperclip.copy(structure)
    
    # Imprime un mensaje de éxito
    print(f"El archivo '{output_path}' ha sido generado correctamente y su contenido ha sido copiado en el portapapeles")

except OSError as e:
    print(f"Error al trabajar con el archivo: {e}")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
