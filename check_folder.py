import sys
from pathlib import Path

def count_files_recursively(directory_path: str) -> None:
    """
    Cuenta todos los archivos (excluyendo directorios) dentro de la ruta
    especificada y todos sus subdirectorios, e imprime el total.

    :param directory_path: La ruta del directorio a inspeccionar.
    """
    try:
        # Crea un objeto Path a partir de la ruta de entrada
        root_dir = Path(directory_path)

        if not root_dir.is_dir():
            print(f"Error: La ruta '{directory_path}' no es un directorio válido.")
            return

        # 1. Usamos rglob('*') para obtener todos los archivos y directorios de forma recursiva.
        # 2. Usamos un generador de comprensión para iterar y verificar que cada elemento sea un archivo.
        # 3. Contamos los archivos que cumplen la condición.
        
        file_count = sum(1 for item in root_dir.rglob('*') if item.is_file())
        
        print("-" * 40)
        print(f"Ruta inspeccionada: {root_dir.resolve()}")
        print(f"Total de directorios y subdirectorios: {len(list(root_dir.glob('**')))-1}") # Cuenta todos los directorios
        print(f"\nTotal de archivos encontrados: {file_count} 📄")
        print("-" * 40)

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # La ruta a inspeccionar se toma como primer argumento de la línea de comandos.
    # Si no se proporciona un argumento, usa el directorio actual ('.').
    if len(sys.argv) > 1:
        path_to_check = sys.argv[1]
        print(f"Usando el directorio {path_to_check}")
    else:
        path_to_check = '.'
        print("Usando el directorio actual (.) por defecto.")
        
    count_files_recursively(path_to_check)
