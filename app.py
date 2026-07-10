import shutil
import time

import cv2
import numpy as np
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from serial.tools import list_ports


class Ui_MainWindow(object):
    def __init__(self):
        self.cap = None
        self.serial_timer = None
        self.elapsed_pause_time = None
        self.start_time = None
        self.video_file_path = None
        self.output_video = None
        self.paused = None
        self.recording = None
        self.timer = None
        self.btnStop = None
        self.labelCam = None
        self.labelCom = None
        self.btnCerrar = None
        self.btnAbrir = None
        self.labelRecord = None
        self.lblkaxtik = None
        self.editTiempo = None
        self.btnGuardar = None
        self.btnParar = None
        self.btnGrabar = None
        self.labelVideoAnalsiis = None
        self.labelHome = None
        self.btnHome = None
        self.TiltLabel = None
        self.PanLabel = None
        self.TiltDial = None
        self.PanDial = None
        self.labelControl = None
        self.btnSeguimiento = None
        self.labelModo = None
        self.lblContainer = None
        self.label = None
        self.btnManual = None
        self.centralwidget = None
        self.record_timer = None
        self.arduino = None
        self.manualMode = None
        self.following = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnManual = QtWidgets.QPushButton(self.centralwidget)
        self.btnManual.setGeometry(QtCore.QRect(1410, 330, 180, 40))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.btnManual.setFont(font)
        self.btnManual.setStyleSheet("QPushButton#btnManual {\n"
                                     "    background-color: rgb(235, 235, 235);\n"
                                     "    border-radius: 10px;\n"
                                     "    min-width: 10em;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnManual:hover {\n"
                                     "    background-color: rgb(235, 235, 235);   \n"
                                     "    border-style: inset;\n"
                                     "    border-width: 5px;\n"
                                     "    border-color: rgb(217, 217, 217);\n"
                                     "    color: rgb(0, 0, 0);\n"
                                     "    border-style: inset;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnManual:pressed {\n"
                                     "    background-color: rgb(217, 217, 217);\n"
                                     "    color: rgb(0,0,0);\n"
                                     "    border-style: inset;\n"
                                     "}\n"
                                     "\n"
                                     "")
        self.btnManual.setObjectName("btnManual")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1800, 100))
        self.label.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.lblContainer = QtWidgets.QLabel(self.centralwidget)
        self.lblContainer.setGeometry(QtCore.QRect(10, 110, 1380, 760))
        self.lblContainer.setStyleSheet("background-color: rgb(217, 217, 217);\n"
                                        "border-radius:20px;")
        self.lblContainer.setText("")
        self.lblContainer.setObjectName("lblContainer")
        self.labelModo = QtWidgets.QLabel(self.centralwidget)
        self.labelModo.setGeometry(QtCore.QRect(1450, 270, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Evil Empire")
        font.setPointSize(24)
        self.labelModo.setFont(font)
        self.labelModo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelModo.setObjectName("labelModo")
        self.btnSeguimiento = QtWidgets.QPushButton(self.centralwidget)
        self.btnSeguimiento.setGeometry(QtCore.QRect(1600, 330, 180, 40))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(18)
        self.btnSeguimiento.setFont(font)
        self.btnSeguimiento.setStyleSheet("QPushButton#btnSeguimiento {\n"
                                          "    background-color: rgb(235, 235, 235);\n"
                                          "    border-radius: 10px;\n"
                                          "    min-width: 10em;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton#btnSeguimiento:hover {\n"
                                          "    background-color: rgb(235, 235, 235);   \n"
                                          "    border-style: inset;\n"
                                          "    border-width: 5px;\n"
                                          "    border-color: rgb(217, 217, 217);\n"
                                          "    color: rgb(0, 0, 0);\n"
                                          "    border-style: inset;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton#btnSeguimiento:pressed {\n"
                                          "    background-color: rgb(217, 217, 217);\n"
                                          "    color: rgb(0,0,0);\n"
                                          "    border-style: inset;\n"
                                          "}\n"
                                          "")
        self.btnSeguimiento.setObjectName("btnSeguimiento")
        self.labelControl = QtWidgets.QLabel(self.centralwidget)
        self.labelControl.setGeometry(QtCore.QRect(1440, 380, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Evil Empire")
        font.setPointSize(24)
        self.labelControl.setFont(font)
        self.labelControl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelControl.setObjectName("labelControl")
        self.PanDial = QtWidgets.QDial(self.centralwidget)
        self.PanDial.setGeometry(QtCore.QRect(1440, 430, 171, 131))
        self.PanDial.setMaximum(180)
        self.PanDial.setNotchesVisible(True)
        self.PanDial.setObjectName("PanDial")
        self.TiltDial = QtWidgets.QDial(self.centralwidget)
        self.TiltDial.setGeometry(QtCore.QRect(1590, 430, 171, 131))
        self.TiltDial.setMaximum(180)
        self.TiltDial.setNotchesVisible(True)
        self.TiltDial.setObjectName("TiltDial")
        self.PanLabel = QtWidgets.QLabel(self.centralwidget)
        self.PanLabel.setGeometry(QtCore.QRect(1500, 560, 55, 31))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.PanLabel.setFont(font)
        self.PanLabel.setStyleSheet("background-color: rgb(255, 141, 65);\n"
                                    "border-radius: 10px; ")
        self.PanLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PanLabel.setObjectName("PanLabel")
        self.TiltLabel = QtWidgets.QLabel(self.centralwidget)
        self.TiltLabel.setGeometry(QtCore.QRect(1650, 560, 55, 31))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.TiltLabel.setFont(font)
        self.TiltLabel.setStyleSheet("background-color: rgb(255, 141, 65);\n"
                                     "border-radius: 10px; ")
        self.TiltLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TiltLabel.setObjectName("TiltLabel")
        self.btnHome = QtWidgets.QPushButton(self.centralwidget)
        self.btnHome.setGeometry(QtCore.QRect(1410, 650, 172, 41))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.btnHome.setFont(font)
        self.btnHome.setStyleSheet("QPushButton#btnHome {\n"
                                   "    background-color: rgb(235, 235, 235);\n"
                                   "    border-radius: 15px;\n"
                                   "    min-width: 10em;\n"
                                   "    padding: 6px;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton#btnHome:hover {\n"
                                   "    background-color: rgb(255, 232, 149);   \n"
                                   "    color: rgb(0, 0, 0);\n"
                                   "    border-style: inset;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton#btnHome:pressed {\n"
                                   "    background-color:rgb(255, 226, 106);\n"
                                   "    color: rgb(0,0,0);\n"
                                   "    border-style: inset;\n"
                                   "}\n"
                                   "")
        self.btnHome.setObjectName("btnHome")
        self.labelHome = QtWidgets.QLabel(self.centralwidget)
        self.labelHome.setGeometry(QtCore.QRect(1450, 610, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(16)
        self.labelHome.setFont(font)
        self.labelHome.setStyleSheet("border-radius:15px;")
        self.labelHome.setText("")
        self.labelHome.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHome.setObjectName("labelHome")
        self.labelVideoAnalsiis = QtWidgets.QLabel(self.centralwidget)
        self.labelVideoAnalsiis.setGeometry(QtCore.QRect(1450, 700, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Evil Empire")
        font.setPointSize(24)
        self.labelVideoAnalsiis.setFont(font)
        self.labelVideoAnalsiis.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelVideoAnalsiis.setObjectName("labelVideoAnalsiis")
        self.btnGrabar = QtWidgets.QPushButton(self.centralwidget)
        self.btnGrabar.setGeometry(QtCore.QRect(1410, 760, 172, 51))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.btnGrabar.setFont(font)
        self.btnGrabar.setStyleSheet("QPushButton#btnGrabar {\n"
                                     "    background-color: rgb(235, 235, 235);\n"
                                     "    border-radius: 15px;\n"
                                     "    min-width: 10em;\n"
                                     "    padding: 6px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnGrabar:hover {\n"
                                     "    background-color: rgb(187, 255, 192);   \n"
                                     "    color: rgb(0, 0, 0);\n"
                                     "    border-style: inset;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnGrabar:pressed {\n"
                                     "    background-color:rgb(114, 198, 127);\n"
                                     "    color: rgb(0,0,0);\n"
                                     "    border-style: inset;\n"
                                     "}")
        self.btnGrabar.setObjectName("btnGrabar")
        self.btnParar = QtWidgets.QPushButton(self.centralwidget)
        self.btnParar.setGeometry(QtCore.QRect(1410, 820, 172, 51))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.btnParar.setFont(font)
        self.btnParar.setStyleSheet("QPushButton#btnParar {\n"
                                    "    background-color: rgb(235, 235, 235);\n"
                                    "    border-radius: 15px;\n"
                                    "    min-width: 10em;\n"
                                    "    padding: 6px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton#btnParar:hover {\n"
                                    "    background-color:rgb(255, 168, 125);   \n"
                                    "    color: rgb(0, 0, 0);\n"
                                    "    border-style: inset;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton#btnParar:pressed {\n"
                                    "    background-color:rgb(255, 135, 105);\n"
                                    "    color: rgb(0,0,0);\n"
                                    "    border-style: inset;\n"
                                    "}")
        self.btnParar.setObjectName("btnParar")
        self.btnGuardar = QtWidgets.QPushButton(self.centralwidget)
        self.btnGuardar.setGeometry(QtCore.QRect(1590, 820, 172, 51))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.btnGuardar.setFont(font)
        self.btnGuardar.setStyleSheet("QPushButton#btnGuardar {\n"
                                      "    background-color: rgb(235, 235, 235);\n"
                                      "    border-radius: 15px;\n"
                                      "    min-width: 10em;\n"
                                      "    padding: 6px;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton#btnGuardar:hover {\n"
                                      "    background-color: rgb(203, 206, 255);   \n"
                                      "    color: rgb(0, 0, 0);\n"
                                      "    border-style: inset;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton#btnGuardar:pressed {\n"
                                      "    background-color:rgb(155, 170, 255);\n"
                                      "    color: rgb(0,0,0);\n"
                                      "    border-style: inset;\n"
                                      "}\n"
                                      "")
        self.btnGuardar.setObjectName("btnGuardar")
        self.editTiempo = QtWidgets.QLineEdit(self.centralwidget)
        self.editTiempo.setGeometry(QtCore.QRect(1590, 760, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.editTiempo.setFont(font)
        self.editTiempo.setStyleSheet("border-radius:15px;")
        self.editTiempo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.editTiempo.setObjectName("editTiempo")
        self.lblkaxtik = QtWidgets.QLabel(self.centralwidget)
        self.lblkaxtik.setGeometry(QtCore.QRect(1510, 10, 271, 81))
        self.lblkaxtik.setStyleSheet("image: url(:/images/KAXTIK.png);\n"
                                     "background-color: rgb(235, 235, 235);")
        self.lblkaxtik.setText("")
        self.lblkaxtik.setPixmap(QtGui.QPixmap(":/images/KAXTIK.png"))
        self.lblkaxtik.setScaledContents(True)
        self.lblkaxtik.setObjectName("lblkaxtik")
        self.labelRecord = QtWidgets.QLabel(self.centralwidget)
        self.labelRecord.setGeometry(QtCore.QRect(1330, 130, 40, 40))
        self.labelRecord.setStyleSheet("border-radius: 20px;\n"
                                       "background-color: rgb(255, 230, 231);")
        self.labelRecord.setText("")
        self.labelRecord.setObjectName("labelRecord")
        self.btnAbrir = QtWidgets.QPushButton(self.centralwidget)
        self.btnAbrir.setGeometry(QtCore.QRect(1540, 200, 60, 60))
        self.btnAbrir.setStyleSheet("QPushButton#btnAbrir {\n"
                                    "    background-color: rgb(231, 255, 234);\n"
                                    "    border-radius: 30px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton#btnAbrir:hover {\n"
                                    "    background-color: rgb(126, 255, 124);   \n"
                                    "    color: rgb(0, 0, 0);\n"
                                    "    border-style: inset;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton#btnAbrir:pressed {\n"
                                    "    background-color:rgb(85, 255, 0);\n"
                                    "    color: rgb(0,0,0);\n"
                                    "    border-style: inset;\n"
                                    "}")
        self.btnAbrir.setText("")
        self.btnAbrir.setObjectName("btnAbrir")
        self.btnCerrar = QtWidgets.QPushButton(self.centralwidget)
        self.btnCerrar.setGeometry(QtCore.QRect(1610, 200, 60, 60))
        self.btnCerrar.setStyleSheet("QPushButton#btnCerrar {\n"
                                     "    background-color: rgb(255, 230, 226);\n"
                                     "    border-radius: 30px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnCerrar:hover {\n"
                                     "    background-color: rgb(255, 174, 174);   \n"
                                     "    color: rgb(0, 0, 0);\n"
                                     "    border-style: inset;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton#btnCerrar:pressed {\n"
                                     "    background-color: rgb(255, 88, 88);\n"
                                     "    color: rgb(0,0,0);\n"
                                     "    border-style: inset;\n"
                                     "}")
        self.btnCerrar.setText("")
        self.btnCerrar.setObjectName("btnCerrar")
        self.labelCom = QtWidgets.QLabel(self.centralwidget)
        self.labelCom.setGeometry(QtCore.QRect(1450, 130, 311, 51))
        font = QtGui.QFont()
        font.setFamily("Evil Empire")
        font.setPointSize(24)
        self.labelCom.setFont(font)
        self.labelCom.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelCom.setObjectName("labelCom")
        self.labelCam = QtWidgets.QLabel(self.centralwidget)
        self.labelCam.setGeometry(QtCore.QRect(30, 130, 1280, 720))
        self.labelCam.setText("")
        self.labelCam.setObjectName("labelCam")
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStop.setGeometry(QtCore.QRect(1600, 650, 172, 41))
        font = QtGui.QFont()
        font.setFamily("F.C. BARCELONA")
        font.setPointSize(16)
        self.btnStop.setFont(font)
        self.btnStop.setStyleSheet("QPushButton#btnStop {\n"
                                   "    background-color: rgb(235, 235, 235);\n"
                                   "    border-radius: 15px;\n"
                                   "    min-width: 10em;\n"
                                   "    padding: 6px;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton#btnStop:hover {\n"
                                   "    background-color:rgb(255, 165, 61); \n"
                                   "    color: rgb(0, 0, 0);\n"
                                   "    border-style: inset;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton#btnStop:pressed {\n"
                                   "    background-color:rgb(255, 124, 16);\n"
                                   "    color: rgb(0,0,0);\n"
                                   "    border-style: inset;\n"
                                   "}")
        self.btnStop.setObjectName("btnStop")
        self.label.raise_()
        self.lblContainer.raise_()
        self.btnManual.raise_()
        self.labelModo.raise_()
        self.btnSeguimiento.raise_()
        self.labelControl.raise_()
        self.PanDial.raise_()
        self.TiltDial.raise_()
        self.PanLabel.raise_()
        self.TiltLabel.raise_()
        self.btnHome.raise_()
        self.labelHome.raise_()
        self.labelVideoAnalsiis.raise_()
        self.btnGrabar.raise_()
        self.btnParar.raise_()
        self.btnGuardar.raise_()
        self.editTiempo.raise_()
        self.lblkaxtik.raise_()
        self.labelRecord.raise_()
        self.btnAbrir.raise_()
        self.btnCerrar.raise_()
        self.labelCom.raise_()
        self.labelCam.raise_()
        self.btnStop.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # TERMINA CÓDIGO DERIVADO DE QT DESIGNER

        # Establecer valores iniciales de los diales
        self.PanDial.setValue(90)  # Valor inicial para Pan
        self.TiltDial.setValue(90)  # Valor inicial para Tilt

        self.update_label_home()

        # COMIENZA CÓDIGO DERIVADO DEL FUNCIONAMIENTO DE LA APLICACIÓN
        # Configuración de la captura de imagen
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None

        # Configuración del grabador de video
        self.recording = False
        self.paused = False
        self.output_video = None
        self.video_file_path = None  # Ruta del archivo de video

        # Conectar con botones de funciones
        self.btnAbrir.clicked.connect(self.start_video)
        self.btnCerrar.clicked.connect(self.stop_video)
        self.btnGrabar.clicked.connect(self.toggle_recording)
        self.btnParar.clicked.connect(self.toggle_pause)
        self.btnGuardar.clicked.connect(self.save_video)
        self.btnManual.clicked.connect(self.activate_manual_mode)
        self.btnHome.clicked.connect(self.activate_home_mode)
        self.btnSeguimiento.clicked.connect(self.activate_follow_mode)
        self.btnStop.clicked.connect(self.reset_modes)

        # Conectar Dial's a las funciones de control de servos
        self.PanDial.valueChanged.connect(self.update_pan_servo)
        self.TiltDial.valueChanged.connect(self.update_tilt_servo)

        # Conectar dials a la función que actualiza el labelHome
        self.PanDial.valueChanged.connect(self.update_label_home)
        self.TiltDial.valueChanged.connect(self.update_label_home)

        # Timer para actualización de video
        self.record_timer = QTimer()
        self.record_timer.timeout.connect(self.update_recording_time)
        self.start_time = None
        self.elapsed_pause_time = 0

        # Inicializar la comunicación serial con la placa Arduino
        self.arduino = None
        self.initialize_serial_connection()

        # Timer para enviar los datos de los dials continuamente
        self.serial_timer = QTimer()
        self.serial_timer.timeout.connect(self.send_servo_commands)
        self.serial_timer.start(50)

        # Variables para seguimiento
        self.following = False
        self.manualMode = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KAXTIK"))
        self.btnManual.setText(_translate("MainWindow", "MANUAL"))
        self.labelModo.setText(_translate("MainWindow", "MODO DE GRABACIÓN"))
        self.btnSeguimiento.setText(_translate("MainWindow", "SEGUIMIENTO"))
        self.labelControl.setText(_translate("MainWindow", "CONTROL DE KAXTIK"))
        self.PanLabel.setText(_translate("MainWindow", "PAN"))
        self.TiltLabel.setText(_translate("MainWindow", "TILT"))
        self.btnHome.setText(_translate("MainWindow", "HOME"))
        self.labelVideoAnalsiis.setText(_translate("MainWindow", "VIDEO ANÁLISIS"))
        self.btnGrabar.setText(_translate("MainWindow", "GRABAR"))
        self.btnParar.setText(_translate("MainWindow", "PARAR"))
        self.btnGuardar.setText(_translate("MainWindow", "GUARDAR"))
        self.labelCom.setText(_translate("MainWindow", "COMUNICACIÓN"))
        self.btnStop.setText(_translate("MainWindow", "STOP"))

    def start_video(self):
        self.cap = cv2.VideoCapture(0)
        #self.cap.set = (cv2.CAP_PROP_FPS, 60)
        self.timer.start(20)
        self.labelRecord.setStyleSheet("border-radius: 20px;\n"
                                       "background-color: rgb(255, 0, 0);")

    def stop_video(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.clear_label()
        self.reset_buttons_and_labels()
        if self.recording:
            self.stop_recording()

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.paused = False
            self.elapsed_pause_time = 0
            self.start_time = time.time()
            self.record_timer.start(1000)

            # Configuración para Grabar el video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para MP4
            self.video_file_path = 'temp_video.mp4'
            self.output_video = cv2.VideoWriter(self.video_file_path, fourcc, 20.0,
                                                (self.labelCam.width(), self.labelCam.height()))
            self.btnGrabar.setText("GRABANDO...")
            self.btnParar.setText("PAUSAR")
            self.labelRecord.setStyleSheet("border-radius: 20px;\n"
                                           "background-color: rgb(0, 255, 0);")  # Rojo intenso

    def toggle_pause(self):
        if self.recording:
            if not self.paused:
                self.paused = True
                self.record_timer.stop()
                self.btnParar.setText("REANUDAR")
                self.btnGrabar.setText("ESPERANDO...")
                self.labelRecord.setStyleSheet("border-radius: 20px; \n"
                                               "background-color: rgb(255,255,0);")
                self.elapsed_pause_time = time.time() - self.start_time
            else:
                self.paused = False
                self.start_time = time.time() - self.elapsed_pause_time
                self.record_timer.start(1000)
                self.btnParar.setText("PAUSAR")
                self.btnGrabar.setText("GRABANDO...")
                self.labelRecord.setStyleSheet("border-radius: 20px; \n"
                                               "background-color: rgb(0,255,0);")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.paused = False
            self.record_timer.stop()
            if self.output_video:
                self.output_video.release()
                self.output_video = None
            self.editTiempo.setText("00:00")
            self.reset_buttons_and_labels()
            # Guardar el video al detener la grabación
            self.save_video()

    def save_video(self):
        global save_path
        if self.video_file_path:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            save_path, _ = QFileDialog.getSaveFileName(None, "Guardar Video", "",
                                                       "Video Files (*mp4)", options=options)
        if save_path:
            try:
                # Renombrar el archivo temporal al destino seleccionado
                shutil.move(self.video_file_path, save_path)
                QMessageBox.information(None, "Guardar Video",
                                        f"Video guardado exitosamente en: {save_path}")
                self.video_file_path = None
            except Exception as e:
                QMessageBox.warning(None, "Guardar Video", f"Error al guardar el video: {e}")

    def update_recording_time(self):
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.editTiempo.setText(f"{minutes:02}:{seconds:02}")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.following:
                frame = self.follow_color(frame)

            # Escalar el frame al tamaño de labelCam
            resized_frame = cv2.resize(frame, (self.labelCam.width(), self.labelCam.height()))

            h, w, ch = resized_frame.shape
            bytes_per_line = ch * w
            image = QImage(resized_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # Mostrar la imagen escalada en labelCam
            self.labelCam.setPixmap(pixmap)

            if self.recording and not self.paused and self.output_video is not None:
                frame_bgr = cv2.cvtColor(resized_frame, cv2.COLOR_RGB2BGR)
                self.output_video.write(frame_bgr)

    def follow_color(self, frame):

        # Aplicar el flip al frame para que los movimientos coincidan con la realidad
        frame = cv2.flip(frame, 1)

        # Definir los límites del color verde
        low_green = np.array([35, 100, 100])
        high_green = np.array([85, 255, 255])

        # Convertir el frame a HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear una máscara para el color verde
        maskGreen = cv2.inRange(frameHSV, low_green, high_green)
        maskGreen = cv2.erode(maskGreen, None, iterations=2)
        maskGreen = cv2.dilate(maskGreen, None, iterations=2)

        # Encontrar contornos
        contours, _ = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        if contours:
            # Seleccionar el contorno con mayor área
            maxCont = max(contours, key=cv2.contourArea)

            # Dibujar un bounding box en el área detectada
            x, y, w, h = cv2.boundingRect(maxCont)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calcular el centro del contorno
            cx = x + w // 2
            cy = y + h // 2

            # Dibujar un punto en el centro
            cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)

            # Determinar la acción a tomar basada en la posición del centro del contorno
            an, al, _ = frame.shape  # Ancho y alto del frame
            centrox = an // 2
            centroy = al // 2

            # Definir la zona muerta alrededor del centro
            dead_zone_size = 60  # Ajusta este valor según sea necesario

            if self.arduino:
                # Bandera para saber si se debe detener
                should_stop = True

                if cx < centrox - dead_zone_size:
                    self.arduino.write(b'i')  # Mover a la izquierda
                    should_stop = False
                elif cx > centrox + dead_zone_size:
                    self.arduino.write(b'd')  # Mover a la derecha
                    should_stop = False

                if cy < centroy - dead_zone_size:
                    self.arduino.write(b'u')  # Mover hacia arriba
                    should_stop = False
                elif cy > centroy + dead_zone_size:
                    self.arduino.write(b'b')  # Mover hacia abajo

                # Si el objeto está centrado, detener los motores
                if should_stop:
                    self.arduino.write(b'x')  # Comando para detener los motores

        return frame

    def clear_label(self):
        self.labelCam.clear()

    def reset_buttons_and_labels(self):
        self.btnGrabar.setText("GRABAR")
        self.btnParar.setText("PAUSAR")
        self.labelRecord.setStyleSheet("border-radius: 20px;\n"
                                       "background-color: rgb(255, 230, 231);")

    def activate_manual_mode(self):
        if not self.manualMode:
            self.manualMode = True
            self.following = False
            self.PanDial.setEnabled(True)
            self.TiltDial.setEnabled(True)
            self.btnSeguimiento.setEnabled(False)
            # Enviar el comando M para activar el modo manual en el Arduino
            if self.arduino:
                self.arduino.write(b'M')
        else:
            self.manualMode = False
            self.PanDial.setEnabled(False)
            self.TiltDial.setEnabled(False)
            self.btnSeguimiento.setEnabled(True)
            # NO ENVIAR comandos para djear parados los motores
            self.send_servo_commands()

    def activate_follow_mode(self):
        if not self.following:
            self.following = True
            self.manualMode = False
            self.btnManual.setEnabled(False)
            self.PanDial.setEnabled(False)
            self.TiltDial.setEnabled(False)

            self.btnSeguimiento.setText("DETENER")

            # Enviar el comando 'S' para activar el modo seguimiento en el Arduino
            if self.arduino:
                self.arduino.write(b'S')

        else:
            self.following = False
            self.btnManual.setEnabled(True)
            self.PanDial.setEnabled(False)
            self.TiltDial.setEnabled(False)

            # Cambiar la función del botón de Seguimiento
            self.btnSeguimiento.setText("SEGUIMIENTO")

    def activate_home_mode(self):
        #Enviar el comando H para mover a la posición inicial en el Arduino
        if self.arduino:
            self.arduino.write(b'H')
        #Volver a la posición inicial en la aplicación
        self.reset_to_home()

    def reset_to_home(self):
        self.PanDial.setValue(90)
        self.TiltDial.setValue(90)
        self.update_label_home()
        self.send_servo_commands()

        # Si el botón Home se presiona, desactivar el modo manual
        if self.manualMode:
            self.activate_manual_mode()

    def initialize_serial_connection(self):
        try:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if "Arduino" in port.description:
                    self.arduino = serial.Serial(port.device, 9600, timeout=10)
                    time.sleep(2)
                    print(f"Conexión con Arduino establecida en: {port.device}")
                    return
        except serial.SerialException as e:
            print(f"Error al conectarse con Arduino: {e}")

    def send_servo_commands(self):
        if self.arduino and self.manualMode:
            try:
                pan_value = self.PanDial.value()
                tilt_value = self.TiltDial.value()
                # Enviar los vlores de Pan y Tilt como comandos explícitos
                self.arduino.write(f'P{pan_value}'.encode())
                self.arduino.write(f'T{tilt_value}'.encode())
            except Exception as e:
                print(f"Error al enviar datos al Arduino: {e}")

    def update_label_home(self):
        pan_value = self.PanDial.value()
        tilt_value = self.TiltDial.value()
        self.labelHome.setText(f"{pan_value}°, {tilt_value}°")

    def update_pan_servo(self, value):
        self.send_servo_commands()

    def update_tilt_servo(self, value):
        self.send_servo_commands()

    def reset_modes(self):
        # Resetear todos los modos y controles
        self.manualMode = False
        self.following = False
        self.PanDial.setEnabled(False)
        self.TiltDial.setEnabled(False)
        self.btnManual.setEnabled(True)
        self.btnSeguimiento.setEnabled(True)
        self.btnSeguimiento.setText("SEGUIMIENTO")

        # Enviar el comando 'P' para parar el arduino
        if self.arduino:
            self.arduino.write(b'Q')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
