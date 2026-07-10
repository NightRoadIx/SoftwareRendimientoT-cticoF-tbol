import sys
import cv2
import os
import csv
import io
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel,QFileDialog
from PyQt5.QtCore import QTimer, QDateTime, QProcess
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Aplicacion import Ui_MainWindow
from firebase import firebase
from PDF_C import agregar_fecha_carlos
from PDF import agregar_fecha_oscar
from PDF_S import agregar_fecha_santander

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("  ")
        self.setWindowIcon(QIcon("Imagenes/QuetzalDark.png"))

        # Inicializa la aplicación de Firebase
        self.firebase = firebase.FirebaseApplication("https://trabajoterminal-c-default-rtdb.firebaseio.com/", None)

        # Analsis
        self.video_path = None
        self.cap = None
        self.timer = QTimer()
        self.centralWidget = self.ui.Videos_PP
        self.layout = self.ui.Botones
        self.video_label = self.ui.Video
        self.ui.Archivo.clicked.connect(self.select_video)
        self.ui.Play.clicked.connect(self.play_video)
        self.ui.Pause.clicked.connect(self.pause_video)
        self.ui.Closed.clicked.connect(self.stop_video)
        self.ui.Img.clicked.connect(self.take_snapshot)

        # Plantilla
        self.scroll_area = self.ui.Filtro
        self.central_widget = self.ui.Filtro_jugadores_widget
        self.layout_principal = self.ui.Principal
        self.layout_campos = self.ui.Botones_filtros
        self.scroll_area.setWidgetResizable(True)
        self.layout_principal.addWidget(self.scroll_area)

        self.central_widget_jugadores = QWidget()
        self.scroll_area.setWidget(self.central_widget_jugadores)

        self.layout_jugadores = QGridLayout()
        self.central_widget_jugadores.setLayout(self.layout_jugadores)

        self.txt_nombre = self.ui.Nombre_Jugador
        self.txt_numero = self.ui.Camisa
        self.txt_posicion = self.ui.Posicion

        self.ui.Filtrar.clicked.connect(self.buscar_jugador)
        self.ui.Limpiar.clicked.connect(self.limpiar_campos)

        # Datos de jugadores
        self.jugadores = self.descargar_jugadores()
        self.tamano_recuadro_horizontal = 500  # Ancho del recuadro
        self.tamano_recuadro_vertical = 250  # Alto del recuadro
        self.actualizar_recuadros()

        # Reporte
        self.ui.Imprimir.clicked.connect(self.print_pdf)
        self.process = QProcess(self)
        self.process.finished.connect(self.process_finished)

        self.ui.Imprimir_Carlos.clicked.connect(self.print_pdf1)
        self.process = QProcess(self)
        self.process.finished.connect(self.process_finished2)

        self.ui.Imprimir_Santander.clicked.connect(self.print_pdf3)
        self.process = QProcess(self)
        self.process.finished.connect(self.process_finished3)

        # Botones de la Aplicación
        self.ui.Bienvenido_One.clicked.connect(self.switch_to_Bienvenido_Page)
        self.ui.Bienvenido_Two.clicked.connect(self.switch_to_Bienvenido_Page)
        self.ui.Dashboard_One.clicked.connect(self.switch_to_Dashboard_Page)
        self.ui.Dashboard_Two.clicked.connect(self.switch_to_Dashboard_Page)
        self.ui.Sesiones_One.clicked.connect(self.switch_to_Sesiones_Page)
        self.ui.Sesiones_Two.clicked.connect(self.switch_to_Sesiones_Page)
        self.ui.Plantilla_One.clicked.connect(self.switch_to_Plantilla_Page)
        self.ui.Plantilla_Two.clicked.connect(self.switch_to_Plantilla_Page)
        self.ui.Reporte_One.clicked.connect(self.switch_to_Reportes_Page)
        self.ui.Reporte_Two.clicked.connect(self.switch_to_Reportes_Page)
        self.ui.Analisis_One.clicked.connect(self.switch_to_Analisis_Page)
        self.ui.Analisis_Two.clicked.connect(self.switch_to_Analisis_Page)
        self.ui.C1.clicked.connect(self.switch_to_C_1)
        self.ui.C2.clicked.connect(self.switch_to_C_2)
        self.ui.C3.clicked.connect(self.switch_to_C_3)
        self.ui.C4.clicked.connect(self.switch_to_C_4)
        self.ui.C5.clicked.connect(self.switch_to_C_5)
        self.ui.C6.clicked.connect(self.switch_to_C_6)
        self.ui.C7.clicked.connect(self.switch_to_C_7)
        self.ui.C8.clicked.connect(self.switch_to_C_8)
        self.ui.C9.clicked.connect(self.switch_to_C_9)
        self.ui.C10.clicked.connect(self.switch_to_C_10)
        self.ui.C11.clicked.connect(self.switch_to_C_11)
        self.ui.C12.clicked.connect(self.switch_to_C_12)
        self.ui.C13.clicked.connect(self.switch_to_C_13)
        self.ui.C14.clicked.connect(self.switch_to_C_14)
        self.ui.C15.clicked.connect(self.switch_to_C_15)
        self.ui.C16.clicked.connect(self.switch_to_C_16)
        self.ui.C17.clicked.connect(self.switch_to_C_17)
        self.ui.C18.clicked.connect(self.switch_to_C_18)
        self.ui.C19.clicked.connect(self.switch_to_C_19)
        self.ui.C20.clicked.connect(self.switch_to_C_20)
        self.ui.C21.clicked.connect(self.switch_to_C_21)
        self.ui.C22.clicked.connect(self.switch_to_C_22)
        self.ui.C23.clicked.connect(self.switch_to_C_23)
        self.ui.C24.clicked.connect(self.switch_to_C_24)
        self.ui.C25.clicked.connect(self.switch_to_C_25)
        self.ui.C26.clicked.connect(self.switch_to_C_26)

    def descargar_jugadores(self):
        coleccion = 'Datos_Jugadores'
        nombre_archivo_firebase = 'jugadores'
        contenido = self.firebase.get(f'/{coleccion}/{nombre_archivo_firebase}', None)
        if contenido is not None:
            print(f"Archivo CSV '{nombre_archivo_firebase}' descargado exitosamente desde Firebase")
            return self.csv_a_lista_de_diccionarios(contenido)
        else:
            print(
                f"No se encontró el archivo CSV '{nombre_archivo_firebase}' en la colección '{coleccion}' en Firebase")
            return []

    def csv_a_lista_de_diccionarios(self, contenido_csv):
        f = io.StringIO(contenido_csv)
        reader = csv.DictReader(f)
        lista_de_diccionarios = [fila for fila in reader]
        return lista_de_diccionarios

    def switch_to_Bienvenido_Page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def switch_to_Dashboard_Page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_to_Sesiones_Page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def switch_to_Plantilla_Page(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def switch_to_Reportes_Page(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def switch_to_Analisis_Page(self):
        self.ui.stackedWidget.setCurrentIndex(5)

        # DESDE AQUI COMIENZA REPORTE DE JUGADORES

    def switch_to_C_1(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def switch_to_C_2(self):
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def switch_to_C_3(self):
        self.ui.stackedWidget_2.setCurrentIndex(2)

    def switch_to_C_4(self):
        self.ui.stackedWidget_2.setCurrentIndex(3)

    def switch_to_C_5(self):
        self.ui.stackedWidget_2.setCurrentIndex(4)

    def switch_to_C_6(self):
        self.ui.stackedWidget_2.setCurrentIndex(5)

    def switch_to_C_7(self):
        self.ui.stackedWidget_2.setCurrentIndex(6)

    def switch_to_C_8(self):
        self.ui.stackedWidget_2.setCurrentIndex(7)

    def switch_to_C_9(self):
        self.ui.stackedWidget_2.setCurrentIndex(8)

    def switch_to_C_10(self):
        self.ui.stackedWidget_2.setCurrentIndex(9)

    def switch_to_C_11(self):
        self.ui.stackedWidget_2.setCurrentIndex(10)

    def switch_to_C_12(self):
        self.ui.stackedWidget_2.setCurrentIndex(11)

    def switch_to_C_13(self):
        self.ui.stackedWidget_2.setCurrentIndex(12)

    def switch_to_C_14(self):
        self.ui.stackedWidget_2.setCurrentIndex(13)

    def switch_to_C_15(self):
        self.ui.stackedWidget_2.setCurrentIndex(14)

    def switch_to_C_16(self):
        self.ui.stackedWidget_2.setCurrentIndex(15)

    def switch_to_C_17(self):
        self.ui.stackedWidget_2.setCurrentIndex(16)

    def switch_to_C_18(self):
        self.ui.stackedWidget_2.setCurrentIndex(17)

    def switch_to_C_19(self):
        self.ui.stackedWidget_2.setCurrentIndex(18)

    def switch_to_C_20(self):
        self.ui.stackedWidget_2.setCurrentIndex(19)

    def switch_to_C_21(self):
        self.ui.stackedWidget_2.setCurrentIndex(20)

    def switch_to_C_22(self):
        self.ui.stackedWidget_2.setCurrentIndex(21)

    def switch_to_C_23(self):
        self.ui.stackedWidget_2.setCurrentIndex(22)

    def switch_to_C_24(self):
        self.ui.stackedWidget_2.setCurrentIndex(23)

    def switch_to_C_25(self):
        self.ui.stackedWidget_2.setCurrentIndex(24)

    def switch_to_C_26(self):
        self.ui.stackedWidget_2.setCurrentIndex(25)

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video", "",
                                                   "Archivos de video (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path
            self.cap = cv2.VideoCapture(self.video_path)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)

    def play_video(self):
        if self.cap and not self.timer.isActive():
            self.timer.start(30)

    def pause_video(self):
        if self.timer.isActive():
            self.timer.stop()

    def stop_video(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.timer.isActive():
            self.timer.stop()
        self.video_label.clear()

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(convert_to_qt_format)
                self.video_label.setPixmap(pixmap)
            else:
                self.stop_video()

    def take_snapshot(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd-HH-mm-ss")
                filename = f"Equipo_{current_datetime}.png"
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_name = "Capturas"
                folder_path = os.path.join(desktop_path, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, filename)
                cv2.imwrite(file_path, frame)

    def buscar_jugador(self):
        nombre = self.txt_nombre.text().strip().lower()
        numero = self.txt_numero.text().strip()  # No necesitamos convertirlo a minúsculas
        posicion = self.txt_posicion.text().strip().lower()

        for i in reversed(range(self.layout_jugadores.count())):
            self.layout_jugadores.itemAt(i).widget().setParent(None)

        jugadores_filtrados = []

        for jugador in self.jugadores:
            # Convertimos el número de camiseta a cadena de texto para la comparación
            if (
                    nombre in jugador["nombre"].lower() and
                    (numero == "" or str(
                        jugador["numero"]) == numero) and  # Convertimos el número a cadena para comparar
                    posicion in jugador["posicion"].lower()
            ):
                jugadores_filtrados.append(jugador)

        self.actualizar_recuadros(jugadores_filtrados)

    def limpiar_campos(self):
        self.txt_nombre.clear()
        self.txt_numero.clear()
        self.txt_posicion.clear()
        self.actualizar_recuadros()

    def actualizar_recuadros(self, jugadores=None):
        if jugadores is None:
            jugadores = self.jugadores

        for i in reversed(range(self.layout_jugadores.count())):
            self.layout_jugadores.itemAt(i).widget().setParent(None)

        for idx, jugador in enumerate(jugadores):
            widget_jugador = self.crear_widget_jugador(jugador)
            self.layout_jugadores.addWidget(widget_jugador, idx // 3, idx % 3)

        self.central_widget_jugadores.adjustSize()

    def crear_widget_jugador(self, jugador):
        widget = QWidget()
        color_fondo = self.obtener_color_posicion(jugador["posicion"])
        widget.setStyleSheet(
            f"background-color: {color_fondo}; color: white; border-radius: 10px; padding: 10px; font-size: 16px; font-family: Arial;")
        widget.setFixedSize(self.tamano_recuadro_horizontal, self.tamano_recuadro_vertical)  # Tamaño del recuadro

        layout = QHBoxLayout()

        label_imagen = QLabel()
        pixmap = QPixmap(jugador["imagen"])  # Usa la ruta de la imagen del jugador
        label_imagen.setPixmap(pixmap.scaled(175, 200))  # Tamaño de la imagen dentro del recuadro
        layout.addWidget(label_imagen)

        label_info = QLabel(
            f"<font face='Congenial Black' size='6' color='white'>{jugador['nombre']}</font><br>"
            f"<font face='Berlin Sana FB Demi' size='6' color='white'> {jugador['numero']}|{jugador['posicion']}</font><br>"
            f"<font face='Bahnschrift Condensed' size='60' color='#55ff7f'>Calificación: {jugador['calificacion']}</font>")
        layout.addWidget(label_info)

        widget.setLayout(layout)

        return widget

    def obtener_color_posicion(self, posicion):
        colores = {
            "PO": "#004AAD",  # Portero
            "DFC": "#FF914D",  # Defensa Central
            "LD": "#FF914D",  # Lateral Derecho
            "LI": "#FF914D",  # Lateral Izquierdo
            "MC": "#AAAA00",  # Mediocampista
            "MCD": "#AAAA00",  # Mediocampista Defensivo
            "ED": "#FF3131",  # Extremo Derecho
            "EI": "#FF3131",  # Extremo Izquierdo
            "DEL": "#FF3131",  # Delantero
        }
        return colores.get(posicion, "#34495e")  # Color por defecto

    def print_pdf(self):
        pdf_input = "Plantilla.pdf"  # Ruta del PDF de entrada
        nombre_jugador = "Oscar"  # Nombre del jugador (puedes obtenerlo de algún widget de texto en tu interfaz)
        # Llama a la función agregar_fecha para generar el PDF con la fecha
        agregar_fecha_oscar(pdf_input, nombre_jugador)

    def process_finished(self):
        # Maneja la señal cuando el proceso QProcess ha terminado
        self.process.kill()  # Asegúrate de que el proceso se detenga completamente
        self.process.close()  # Cierra el proceso
        self.process = None  # Limpia la instancia del proceso

    def print_pdf1(self):
        pdf_input = "Plantilla.pdf"  # Ruta del PDF de entrada
        nombre_jugador = "Carlos"  # Nombre del jugador (puedes obtenerlo de algún widget de texto en tu interfaz)

        # Llama a la función agregar_fecha para generar el PDF con la fecha
        agregar_fecha_carlos(pdf_input, nombre_jugador)


    def process_finished2(self):
        # Maneja la señal cuando el proceso QProcess ha terminado
        self.process.kill()  # Asegúrate de que el proceso se detenga completamente
        self.process.close()  # Cierra el proceso
        self.process = None  # Limpia la instancia del proceso

    def print_pdf3(self):
        pdf_input = "Plantilla.pdf"  # Ruta del PDF de entrada
        nombre_jugador = "Santander"  # Nombre del jugador (puedes obtenerlo de algún widget de texto en tu interfaz)

        # Llama a la función agregar_fecha para generar el PDF con la fecha
        agregar_fecha_santander(pdf_input, nombre_jugador)


    def process_finished3(self):
        # Maneja la señal cuando el proceso QProcess ha terminado
        self.process.kill()  # Asegúrate de que el proceso se detenga completamente
        self.process.close()  # Cierra el proceso
        self.process = None  # Limpia la instancia del proceso


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())