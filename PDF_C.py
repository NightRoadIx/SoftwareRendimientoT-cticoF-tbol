import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime
import locale
from firebase import firebase

# Inicializa la aplicación de Firebase
firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

# Variables locales para almacenar los datos descargados de Carlos
pases_acertados_carlos = ''
tiros_acertados_carlos = ''
posicionamiento_carlos = ''
calificacion_carlos = ''
posicion_carlos = ''
t_aciertos_carlos = ''
p_aciertos_carlos = ''

# Función para descargar variables específicas de Carlos desde Firebase
def descargar_variables_carlos():
    global pases_acertados_carlos, tiros_acertados_carlos, posicionamiento_carlos, calificacion_carlos, posicion_carlos, t_aciertos_carlos, p_aciertos_carlos

    # Lista de variables a descargar para Carlos
    variables = ['pases_acertados', 'tiros_acertados', 'posicionamiento', 'calificacion', 'porcentaje_posicion', 'porcentaje_tiros', 'porcentaje_pases']

    # Descargar variables desde Firebase para Carlos
    for variable in variables:
        valor = firebase.get(f'/Evaluaciones/Carlos/{variable}', None)
        if valor is not None:
            if variable == 'pases_acertados':
                pases_acertados_carlos = valor
            elif variable == 'tiros_acertados':
                tiros_acertados_carlos = valor
            elif variable == 'posicionamiento':
                posicionamiento_carlos = valor
            elif variable == 'calificacion':
                calificacion_carlos = valor
            elif variable == 'porcentaje_posicion':
                posicion_carlos = valor
            elif variable == 'porcentaje_tiros':
                t_aciertos_carlos = valor
            elif variable == 'porcentaje_pases':
                p_aciertos_carlos = valor
        else:
            print(f"No se encontró '{variable}' para 'Carlos' en Firebase")

# Función para agregar la fecha y generar el PDF con las variables descargadas de Carlos
def agregar_fecha_carlos(pdf_input, nombre_jugador):
    try:
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        # Obtener la fecha y hora actual en español
        fecha_actual = datetime.now().strftime("%d de %B del %Y")

        # Descargar las variables específicas de Carlos desde Firebase
        descargar_variables_carlos()

        # Crear un nuevo PDF con la fecha y las líneas de texto adicionales
        output = PdfWriter()
        existing_pdf = PdfReader(open(pdf_input, "rb"))

        for page_number in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[page_number]

            # Crear una hoja de Reporte
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=landscape(letter))
            c.setFont("Times-Bold", 26)
            c.setFillColor('#429373')
            c.drawString(340, 562, fecha_actual)

            c.setFont("Helvetica-Bold", 14)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(100, 360, f"{nombre_jugador}-DFC-05")
            c.setFont("Helvetica-Bold", 9)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(70, 345, f"Pases Acertados: {pases_acertados_carlos}")
            c.setFillColor('#429373')
            c.roundRect(173, 345, p_aciertos_carlos, 8, 2, fill=True, stroke=False)

            c.setFillColorRGB(0, 0, 0)
            c.drawString(70, 330, f"Tiros Acertados: {tiros_acertados_carlos}")
            # Barra de progreso después de Texto 2
            c.setFillColor('#429373')
            c.roundRect(173, 330, t_aciertos_carlos, 8, 2, fill=True, stroke=False)

            c.setFillColorRGB(0, 0, 0)
            c.drawString(70, 315, f"Posicionamiento: {posicionamiento_carlos}")
            c.setFillColor('#429373') 
            c.roundRect(173, 315, posicion_carlos, 8, 2, fill=True, stroke=False)

            c.setFillColorRGB(0, 0, 0) 
            c.setFont("Helvetica-Bold", 18)
            c.drawString(90, 293, f"Calificación:")
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor("#FF5500")
            c.drawString(200, 293, f"{calificacion_carlos}")

            # Agregar imágenes
            x1, y1 = 80, 380
            x2, y2 = 538, 65
            x3, y3 = 293, 65
            x4, y4 = 30, 100

            image1_path = os.path.join("C:/Users/josan/Desktop/Aplicacion/carlos.jpg")
            image2_path = os.path.join("C:/Users/josan/Desktop/Aplicacion/Datos/Evaluaciones/Carlos/pases_carlos.png")
            image3_path = os.path.join("C:/Users/josan/Desktop/Aplicacion/Datos/Evaluaciones/Carlos/posicionamiento_carlos.png")
            image4_path = os.path.join("C:/Users/josan/Desktop/Aplicacion/Datos/Evaluaciones/Carlos/rendimiento_carlos.png")

            # Dibujar las imágenes en la hoja
            c.drawImage(image1_path, x1, y1, width=130, height=130)
            c.drawImage(image2_path, x2, y2, width=230, height=450)
            c.drawImage(image3_path, x3, y3, width=230, height=450)
            c.drawImage(image4_path, x4, y4, width=250, height=150)

            c.save()
            packet.seek(0)

            # Agregar la página original del PDF con la fecha y el texto agregados
            page_with_date = PdfReader(packet)
            page.merge_page(page_with_date.pages[0])
            output.add_page(page)

        # Obtener la ruta del escritorio
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Crear una carpeta llamada "Reportes del Evaluado" en el escritorio si no existe
        reportes_folder = os.path.join(desktop_path, 'Reportes del Evaluado', nombre_jugador)
        if not os.path.exists(reportes_folder):
            os.makedirs(reportes_folder)

        # Guardar el PDF con la fecha y hora en el nombre del archivo dentro de la carpeta de Carlos
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_filename = os.path.join(reportes_folder, f"{nombre_jugador}_{fecha_hora_actual}.pdf")
        with open(output_filename, "wb") as f:
            output.write(f)

    except Exception as e:
        print(f"Error: {e}")

# Uso del método para Carlos
#nombre_jugador = "Carlos"
#agregar_fecha_carlos("Plantilla.pdf", nombre_jugador)
