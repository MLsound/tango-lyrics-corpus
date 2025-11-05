import shutil
from pathlib import Path
import os

# ==============================================================================
# 🎯 CONFIGURACIÓN Y UTILIDADES
# ==============================================================================
BASE_DIR = Path('./lyrics')
TEMP_DIR = Path(f"{BASE_DIR}_temp")

def sanitize_name(name: str) -> str:
    """Reemplaza espacios por '_' y puntos por '' para los nombres de carpetas."""
    # Enfoque para CARPETAS: elimina puntos y reemplaza espacios por guiones bajos.
    sanitized = name.replace('.', '').replace(' ', '_')
    return sanitized

def sanitize_filename(filename: str) -> str:
    """Sanea el nombre de un archivo, preservando la extensión si existe."""
    if '.' in filename:
        name_part, *ext_parts = filename.rsplit('.', 1)
        # Sanea solo la parte del nombre: elimina puntos y reemplaza espacios
        name_sanitized = name_part.replace('.', '').replace(' ', '_')
        # Reconstruye el nombre con su extensión original (si la tiene)
        return f"{name_sanitized}.{ext_parts[0]}" if ext_parts else name_sanitized
    else:
        # Si no hay extensión (es solo un nombre de carpeta o un archivo sin extensión)
        return filename.replace('.', '').replace(' ', '_')

def rename_files_recursively(directory: Path):
    """Sanea los nombres de todos los archivos dentro de un directorio, recursivamente."""
    for root, _, files in os.walk(directory, topdown=False):
        for name in files:
            original_path = Path(root) / name
            new_name = sanitize_filename(name)
            
            if name != new_name:
                new_path = Path(root) / new_name
                try:
                    original_path.rename(new_path)
                    # print(f"    Renombrado: {name} -> {new_name}")
                except OSError as e:
                    print(f"    ⚠️ Error al renombrar '{original_path}': {e}")


def organizar_archivos(gnr_dict: dict):
    """Organiza las carpetas basándose en el mapeo de subgéneros a géneros principales."""
    if not gnr_dict:
        print("No se pudo cargar la configuración de géneros. Abortando.")
        return

    print(f"Iniciando reorganización de carpetas en: {BASE_DIR}")
    print("-" * 50)
    
    # --- 1. Saneamiento y Creación de Estructura de Géneros en TEMP ---
    print(f"Construyendo estructura temporal en: {TEMP_DIR}")
    shutil.rmtree(TEMP_DIR, ignore_errors=True) 
    TEMP_DIR.mkdir()

    main_genre_map = {}
    
    # 1a. Crear las carpetas de Género Principal saneadas en TEMP_DIR
    for main_genre in gnr_dict.keys():
        main_genre_sanitized = sanitize_name(main_genre)
        main_genre_map[main_genre] = main_genre_sanitized
        
        destination_dir = TEMP_DIR / main_genre_sanitized
        destination_dir.mkdir(exist_ok=True)
        print(f"  ✅ Carpeta de género creada: '{main_genre_sanitized}'")

    print("-" * 50)

    # --- 2. Mapeo Subgénero SANEADO -> Género Principal Saneado (¡CORRECCIÓN CLAVE!) ---
    # Usamos el nombre saneado del subgénero de la configuración como clave para la búsqueda.
    subgenre_sanitized_to_main_genre = {}
    for main_genre_original, data in gnr_dict.items():
        main_genre_sanitized = main_genre_map[main_genre_original]
        for subgenre_original in data['sub']:
            # La clave de búsqueda es la versión saneada del nombre de la configuración
            subgenre_key = sanitize_name(subgenre_original) 
            subgenre_sanitized_to_main_genre[subgenre_key] = main_genre_sanitized

    # --- 3. Copiar y Sanear Archivos en el Directorio Temporal ---
    print("Copiando y saneando carpetas de subgénero a la estructura temporal...")
    
    for source_subgenre_folder in BASE_DIR.iterdir():
        if source_subgenre_folder.is_dir() and source_subgenre_folder.name != TEMP_DIR.name:
            
            subgenre_name_original_disk = source_subgenre_folder.name
            
            # ❗ CORRECCIÓN: Saneamos el nombre de la carpeta del disco para la búsqueda.
            # Esto permite que 'Canción_del_litoral' o 'Canción del litoral' se busquen como 'Canción_del_litoral'
            subgenre_name_for_search = sanitize_name(subgenre_name_original_disk) 
            
            if subgenre_name_for_search in subgenre_sanitized_to_main_genre:
                
                main_genre_sanitized = subgenre_sanitized_to_main_genre[subgenre_name_for_search]
                
                # El nombre de la carpeta final será la versión saneada que acabamos de usar.
                subgenre_sanitized = subgenre_name_for_search 
                
                destination_dir = TEMP_DIR / main_genre_sanitized / subgenre_sanitized
                
                print(f"  ➡️ Copiando '{subgenre_name_original_disk}' a '{main_genre_sanitized}/{subgenre_sanitized}'...")
                
                # Copiar toda la estructura de carpetas
                shutil.copytree(str(source_subgenre_folder), str(destination_dir), dirs_exist_ok=True)
                
                # Saneamiento recursivo de ARCHIVOS después de la copia
                print(f"  🧹 Saneando nombres de archivos dentro de '{destination_dir.name}'...")
                rename_files_recursively(destination_dir)

            else:
                print(f"  ⚠️ Advertencia: Carpeta no reconocida como subgénero: '{subgenre_name_original_disk}'")

    # --- 4. Fase Final: Reemplazar el directorio base ---
    print("-" * 50)
    print(f"Fase Final: Reemplazando '{BASE_DIR}' con la estructura saneada de '{TEMP_DIR}'.")
    
    # 4a. Limpiamos el directorio base 
    shutil.rmtree(BASE_DIR, ignore_errors=True)
    
    # 4b. Renombramos el directorio temporal al nombre del directorio base
    TEMP_DIR.rename(BASE_DIR)
    
    print(f"  ✅ Directorio base '{BASE_DIR}' actualizado con la nueva estructura saneada.")
    print("-" * 50)
    print("¡Proceso de reorganización finalizado! 🎉")

# ==============================================================================
# 🚀 EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    gnr_dict = {
        'Canción': {'idx':1,
                    'sub':['Canción','Canción ciudadana','Canción serrana','Canción criolla','Balada',]},
        'Folklore': {'idx':2,
                    'sub':['Zamba','Estilo','Tonada','Marcha','Chacarera','Gato',
                        'Huella','Triunfo','Chamamé','Triste campero','Pericón',
                        'Aire de bailecito','Aire de malambo','Aire de zamba',
                        'Canción del litoral','Tonada salteña','Tonada campera',
                        'Chamarrita','Lazo','Bailecito','Rezo gaucho','Sobrepaso',
                        'Cueca','Vidalita',]},
        'Foxtrot': {'idx':3,
                    'sub':['Foxtrot','Shimmy','Fox charleston','Fox Bolero',]},
        'Milonga': {'idx':4,
                    'sub':['Milonga','Candombe','Milonga candombe','Milongón',
                        'Murga','Murga candombe','Cifra']},
        'Otros ritmos': {'idx':5,
                    'sub':['Bolero','Rumba','Guajira','Bambuco','Corrido','Ranchera',
                        'Clásico','Melodía','Shotis','Polca','Fado','Tarantella',
                        'Mazurca','Habanera','Pasodoble','Jota','Java canción']},
        'Poema': {'idx':6,
                    'sub':['Poema','Poema lunfardo','Poema evocativo','Recitado cómico',]},
        'Tango': {'idx':7,
                    'sub':['Tango','Arr. en tango','Tango balada',
                        'Canción-tango','Tango-estilo','Tango-chamamé']},
        'Vals': {'idx':8,
                    'sub': ['Vals','Vals peruano','Arr. en vals','Canción-vals']},
    }
    
    organizar_archivos(gnr_dict)