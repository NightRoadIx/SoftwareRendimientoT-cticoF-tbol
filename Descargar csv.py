from firebase import firebase

# Firebase
firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

# Función para descargar archivos CSV desde Firebase
def descargar_csv(archivos):
    for archivo in archivos:
        coleccion = archivo['coleccion']
        coleccion2 = archivo['coleccion2']
        nombre_archivo = archivo['nombre_archivo']
        nombre_archivo_local = archivo.get('nombre_archivo_local', nombre_archivo)

        # Obtener el contenido del archivo CSV de Firebase
        contenido = firebase.get(f'/{coleccion}/{coleccion2}/{nombre_archivo}', None)
        if contenido is not None:
            # Convertir el contenido a una cadena
            contenido_str = contenido.strip()

            # Escribir el contenido en un archivo CSV local
            with open(nombre_archivo_local, 'w') as file:
                file.write(contenido_str)
            print(f"Archivo CSV '{nombre_archivo}' descargado exitosamente como '{nombre_archivo_local}' desde Firebase")
        else:
            print(f"No se encontró el archivo CSV '{nombre_archivo}' en la colección '{coleccion}/{coleccion2}' en Firebase")

# Lista de archivos CSV a descargar desde Firebase
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

# Llamar a la función para descargar los archivos CSV
descargar_csv(archivos)
