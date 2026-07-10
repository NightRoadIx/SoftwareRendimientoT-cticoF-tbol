import os
import firebase_admin
from firebase_admin import credentials, storage

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("C:/Users/josan/Desktop/Evaluacion Metricas/trabajoterminal-c-firebase-adminsdk-uvmwc-52b9d54ab2.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://trabajoterminal-c-default-rtdb.firebaseio.com/",
    'storageBucket': "trabajoterminal-c.appspot.com"
})

bucket = storage.bucket()

# Diccionario con las carpetas y archivos que se van a descargar
images_to_download = {
    'carlos': {
        'rendimiento_carlos.png': 'rendimiento_carlos.png',
        'posicionamiento_carlos.png': 'posicionamiento_carlos.png',
        'pases_carlos.png': 'pases_carlos.png'
    },
    'oscar': {
        'rendimiento_oscar.png': 'rendimiento_oscar.png',
        'posicionamiento_oscar.jpeg': 'posicionamiento_oscar.jpeg',
        'pases_oscar.jpeg': 'pases_oscar.jpeg'
    },
    'santander': {
        'rendimiento_santander.png': 'rendimiento_santander.png',
        'posicionamiento_santander.jpeg': 'posicionamiento_santander.jpeg',
        'pases_santander.jpeg': 'pases_santander.jpeg'
    }
}

def download_image(blob_name, destination_folder):
    """Descarga un archivo de Firebase Storage."""
    blob = bucket.blob(blob_name)
    destination_file_name = os.path.join(destination_folder, blob_name.split('/')[-1])
    if not os.path.exists(os.path.dirname(destination_file_name)):
        os.makedirs(os.path.dirname(destination_file_name))
    blob.download_to_filename(destination_file_name)
    print(f"Archivo descargado exitosamente a {destination_file_name}")

if __name__ == "__main__":
    for folder, files in images_to_download.items():
        for blob_name, destination_filename in files.items():
            blob_path = f'{folder}/{blob_name}'
            destination_folder = f'C:/Users/josan/Desktop/Aplicacion/Datos/Evaluaciones/{folder}/'
            print(f"Descargando {blob_path} a {destination_folder}...")
            download_image(blob_path, destination_folder)
