from firebase import firebase
import os

# Inicializa la aplicación de Firebase
firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

# Función para subir o actualizar archivos CSV en Firebase
def subir_actualizar_csv(archivos):
    script_dir = os.path.dirname(__file__)  
    for archivo in archivos:
        coleccion = archivo['coleccion']
        coleccion2 = archivo['coleccion2']
        nombre_archivo = archivo['nombre_archivo']
        nombre_archivo_local = archivo['nombre_archivo_local']
        ruta_csv = os.path.join(script_dir, nombre_archivo_local)  
        
        # Leer el contenido del nuevo archivo CSV
        with open(ruta_csv, 'r') as file:
            nuevo_contenido = file.read()

        # Verificar si el archivo ya existe en Firebase
        contenido_existente = firebase.get(f'/{coleccion}/{coleccion2}/{nombre_archivo}', None)
        if contenido_existente is not None:
            # Si el archivo existe, actualizar su contenido en Firebase
            firebase.put(f'/{coleccion}/{coleccion2}', nombre_archivo, nuevo_contenido)
            print(f"Archivo CSV '{nombre_archivo}' actualizado exitosamente en Firebase")
        else:
            # Si el archivo no existe, subirlo a Firebase como un nuevo archivo
            firebase.post(f'/{coleccion}/{coleccion2}', {nombre_archivo: nuevo_contenido})
            print(f"Archivo CSV '{nombre_archivo}' subido exitosamente a Firebase")

# Lista de archivos CSV para subir o actualizar en Firebase
archivos = [
    {
        'coleccion': 'Coordenadas',
        'coleccion2': 'centroid_coordinates_pases',
        'nombre_archivo': '-O0b1Z1Dj7VIQNFJ4gQY',
        'nombre_archivo_local': 'coordenadas_pases.csv'
    },
    {
        'coleccion': 'Coordenadas',
        'coleccion2': 'centroid_coordinates_posicionamiento',
        'nombre_archivo': '-O0b1ZTAI9vcuz6Dm7TZ',
        'nombre_archivo_local': 'coordenadas_posicionamiento.csv'
    },
    {
        'coleccion': 'Coordenadas',
        'coleccion2': 'centroid_coordinates_tiros',
        'nombre_archivo': '-O0b1Z_IJMzND1SShczl',
        'nombre_archivo_local': 'coordenadas_tiros.csv'
    }
]

# Llamar a la función para subir o actualizar los archivos CSV en Firebase
subir_actualizar_csv(archivos)
