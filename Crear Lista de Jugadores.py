import csv
from firebase import firebase

# Inicializa la aplicación de Firebase
firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

# Lista de jugadores
jugadores = [
    {"numero": 1, "nombre": "Iker Salinas", "posicion": "PO", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 13, "nombre": "Alberto Huerta", "posicion": "PO", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 26, "nombre": "Akio Honda", "posicion": "PO", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 3, "nombre": "Mauricio González", "posicion": "DFC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 15, "nombre": "Roberto Castillo", "posicion": "DFC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 23, "nombre": "Adrian Días", "posicion": "DFC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 18, "nombre": "Hugo Hernández", "posicion": "LD", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 2, "nombre": "Oscar Hernández", "posicion": "DFC", "calificacion": '6.7', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/Oscar.png"},
    {"numero": 20, "nombre": "Gerson Hernández", "posicion": "LI", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 21, "nombre": "Rafael Hernández", "posicion": "MC", "calificacion": 'NP', "imagen":"C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 5, "nombre": "Carlos Leal", "posicion": "DFC", "calificacion": '7.75', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/carlos.png"},
    {"numero": 8, "nombre": "Diego Mártinez", "posicion": "MCD", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 12, "nombre": "Dylan Dámian", "posicion": "MC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 14, "nombre": "Arturo Fernández", "posicion": "MC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 10, "nombre": "Lionel Ortega", "posicion": "DEL", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 7, "nombre": "Antonio Peréz", "posicion": "DEL", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 9, "nombre": "Martin Salas", "posicion": "DEL", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 11, "nombre": "Usiel Rodríguez", "posicion": "EI", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 17, "nombre": "Francisco Fragoso", "posicion": "EI", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 19, "nombre": "Pedro Escudero", "posicion": "EI", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 22, "nombre": "JJ Santander", "posicion": "LD", "calificacion": '6.0', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/Santander.png"},
    {"numero": 24, "nombre": "Mateo Fernández", "posicion": "MC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 27, "nombre": "Cesar Fuentes", "posicion": "MC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
    {"numero": 28, "nombre": "Jorge Sánchez", "posicion": "MC", "calificacion": 'NP', "imagen": "C:/Users/josan/Desktop/Aplicacion/Datos/Jugadores/PN3.png"},
]

# Nombre del archivo CSV
nombre_archivo_csv = 'jugadores.csv'

# Escribir la lista de jugadores en un archivo CSV usando codificación utf-8
with open(nombre_archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['numero', 'nombre', 'posicion', 'calificacion', 'imagen']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for jugador in jugadores:
        writer.writerow(jugador)

print(f"Archivo CSV '{nombre_archivo_csv}' creado exitosamente.")

# Función para subir un archivo CSV a Firebase
def subir_csv(ruta_csv, coleccion, nombre_archivo):
    with open(ruta_csv, 'r', encoding='utf-8') as file:
        contenido = file.read()
    firebase.put(f'/{coleccion}', nombre_archivo, contenido)
    print(f"Archivo CSV '{nombre_archivo}' subido exitosamente a Firebase")

# Subir el archivo CSV a Firebase
coleccion = 'Datos_Jugadores'
nombre_archivo_firebase = 'jugadores'
subir_csv(nombre_archivo_csv, coleccion, nombre_archivo_firebase)

# Función para descargar un archivo CSV desde Firebase y guardarlo en una variable
def descargar_csv_a_variable(coleccion, nombre_archivo_firebase):
    contenido = firebase.get(f'/{coleccion}/{nombre_archivo_firebase}', None)
    if contenido is not None:
        print(f"Archivo CSV '{nombre_archivo_firebase}' descargado exitosamente desde Firebase")
        return contenido
    else:
        print(f"No se encontró el archivo CSV '{nombre_archivo_firebase}' en la colección '{coleccion}' en Firebase")
        return None

# Descargar el archivo CSV desde Firebase y guardarlo en una variable
contenido_csv = descargar_csv_a_variable(coleccion, nombre_archivo_firebase)

# Imprimir el contenido del archivo CSV descargado
print("Contenido del CSV descargado:")
print(contenido_csv)

# Función para descargar un archivo CSV desde Firebase y guardarlo en una variable
def descargar_csv_a_variable(coleccion, nombre_archivo_firebase):
    contenido = firebase.get(f'/{coleccion}/{nombre_archivo_firebase}', None)
    if contenido is not None:
        print(f"Archivo CSV '{nombre_archivo_firebase}' descargado exitosamente desde Firebase")
        return contenido
    else:
        print(f"No se encontró el archivo CSV '{nombre_archivo_firebase}' en la colección '{coleccion}' en Firebase")
        return None

# Descargar el archivo CSV desde Firebase y guardarlo en una variable
Jugadores = descargar_csv_a_variable(coleccion, nombre_archivo_firebase)

# Imprimir el contenido del archivo CSV descargado
print("Contenido del CSV descargado:")
print(Jugadores)
