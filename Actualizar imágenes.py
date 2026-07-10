import os
import firebase_admin
from firebase_admin import credentials, storage

# Inicializar Firebase
cred = credentials.Certificate("C:/Users/josan/Desktop/Evaluacion Metricas/trabajoterminal-c-firebase-adminsdk-uvmwc-52b9d54ab2.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://trabajoterminal-c-default-rtdb.firebaseio.com/",
    'storageBucket': "trabajoterminal-c.appspot.com"
})

bucket = storage.bucket()

# Diccionario con las carpetas y archivos que se van a subir y sobrescribir
images_to_upload = {
    'carlos': {
        'rendimiento_carlos.png': "C:/Users/josan/Desktop/Imagenes/Carlos/rendimiento_carlos.png",
        'posicionamiento_carlos.png': "C:/Users/josan/Desktop/Imagenes/Carlos/posicionamiento_carlos.png",
        'pases_carlos.png': "C:/Users/josan/Desktop/Imagenes/Carlos/pases_carlos.png"
    },
    'oscar': {
        'rendimiento_oscar.png': "C:/Users/josan/Desktop/Imagenes/Oscar/rendimiento_oscar.png",
        'posicionamiento_oscar.jpeg': "C:/Users/josan/Desktop/Imagenes/Oscar/posicionamiento_oscar.jpeg",
        'pases_oscar.jpeg': "C:/Users/josan/Desktop/Imagenes/Oscar/pases_oscar.jpeg"
    },
    'santander': {
        'rendimiento_santander.png':  "C:/Users/josan/Desktop/Imagenes/Santander/rendimiento_santander.png",
        'posicionamiento_santander.jpeg': "C:/Users/josan/Desktop/Imagenes/Santander/posicionamiento_santander.jpeg",
        'pases_santander.jpeg': "C:/Users/josan/Desktop/Imagenes/Santander/pases_santander.jpeg"
    }
}

def upload_image(file_path, blob_name):
    """Sube un archivo a Firebase Storage sobrescribiendo el existente si es necesario."""
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    print(f"Archivo subido exitosamente a Firebase Storage con nombre: {blob_name}")

if __name__ == "__main__":
    for folder, files in images_to_upload.items():
        for blob_name, file_path in files.items():
            blob_path = f'{folder}/{blob_name}'
            print(f"Subiendo {file_path} a Firebase Storage con nombre: {blob_path}...")
            upload_image(file_path, blob_path)
