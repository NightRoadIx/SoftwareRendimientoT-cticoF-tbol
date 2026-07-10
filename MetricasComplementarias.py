import sys
import cv2
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = []
        self.start_point = None
        self.current_mode = None

        self.setWindowTitle("MÉTRICAS AUXILIARES")
        self.setGeometry(100, 100, 1200, 600)

        self.initUI()

    def initUI(self):
        # Layout principal
        main_layout = QHBoxLayout()

        # Layout para la imagen y controles
        left_layout = QVBoxLayout()

        # Cargar y mostrar imagen
        self.label = QLabel(self)
        pitch_pixmap = QPixmap("pitch.png")
        self.original_size = pitch_pixmap.size()
        self.label.setPixmap(pitch_pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label.mousePressEvent = self.get_click
        left_layout.addWidget(self.label)

        # ComboBox para seleccionar el tipo de imagen
        self.image_combo = QComboBox(self)
        self.image_combo.addItems(["pitch.png", "Libre.jpeg", "Coberturas.jpeg", "Duelos.jpeg"])
        self.image_combo.currentIndexChanged.connect(self.change_image)
        left_layout.addWidget(QLabel("SELECCIONAR TIPO DE IMAGEN:"))
        left_layout.addWidget(self.image_combo)

        # Selector de jugadores
        self.player_combo = QComboBox(self)
        self.player_combo.addItems(["Oscar", "A", "B", "Carlos", "Santander"])
        left_layout.addWidget(QLabel("ELEGIR JUGADOR:"))
        left_layout.addWidget(self.player_combo)

        # Botones de modo
        left_layout.addWidget(QLabel("MODO:"))
        self.pass_button = QPushButton("COBERTURA")
        self.pass_button.clicked.connect(lambda: self.set_mode("Pass"))
        left_layout.addWidget(self.pass_button)

        self.shot_button = QPushButton("POSICIÓN")
        self.shot_button.clicked.connect(lambda: self.set_mode("Position"))
        left_layout.addWidget(self.shot_button)

        self.tackle_button = QPushButton("RECUPERACIÓN")
        self.tackle_button.clicked.connect(lambda: self.set_mode("Tackle"))
        left_layout.addWidget(self.tackle_button)

        self.foul_button = QPushButton("FALTA")
        self.foul_button.clicked.connect(lambda: self.set_mode("Foul"))
        left_layout.addWidget(self.foul_button)

        # Layout para la tabla y botones
        right_layout = QVBoxLayout()

        # Tabla para mostrar datos
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["X1", "Y1", "X2", "Y2", "Modo", "Jugador"])
        right_layout.addWidget(self.table)

        # Botones de acción
        self.modify_button = QPushButton("MODIFICAR")
        self.modify_button.setStyleSheet("background-color: yellow")
        right_layout.addWidget(self.modify_button)

        self.clear_button = QPushButton("ELIMINAR")
        self.clear_button.setStyleSheet("background-color: red")
        self.clear_button.clicked.connect(self.clear_all_entries)
        right_layout.addWidget(self.clear_button)

        self.save_button = QPushButton("GUARDAR")
        self.save_button.setStyleSheet("background-color: green")
        self.save_button.clicked.connect(self.save_csv)
        right_layout.addWidget(self.save_button)

        # Añadir layouts al layout principal
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Widget principal
        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def set_mode(self, mode):
        self.current_mode = mode
        print(f"Modo seleccionado: {mode}")

    def get_click(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.current_mode and self.player_combo.currentText():
            player = self.player_combo.currentText()
            if self.current_mode == "Pass":
                if not self.start_point:
                    self.start_point = (x, y)
                    print(f"Punto de inicio guardado: ({x}, {y})")
                else:
                    self.data.append([self.start_point[0], self.start_point[1], x, y, self.current_mode, player])
                    self.start_point = None
            elif self.current_mode == "Position":
                self.data.append([x, y, x, y, self.current_mode, player])
            else:
                self.data.append([x, y, x, y, self.current_mode, player])

            self.update_table()
        else:
            print("Por favor, seleccione un modo y un jugador antes de hacer clic.")

    def update_table(self):
        self.table.setRowCount(len(self.data))
        for row_idx, row_data in enumerate(self.data):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def clear_all_entries(self):
        if QMessageBox.question(self, "Confirmar", "¿Está seguro de que desea eliminar todos los datos?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            self.data = []
            self.update_table()

    def save_csv(self):
        if self.data:
            path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo CSV", "", "CSV files (*.csv)")
            if path:
                df = pd.DataFrame(self.data, columns=["X1", "Y1", "X2", "Y2", "Modo", "Jugador"])
                df.to_csv(path, index=False)
                print(f"Datos guardados en {path}")
        else:
            QMessageBox.warning(self, "Error", "No hay datos para guardar.")

    def change_image(self):
        image_path = self.image_combo.currentText()
        # Redimensionar la imagen al tamaño de pitch.png usando OpenCV
        pixmap = self.load_and_resize_image(image_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", f"No se pudo cargar la imagen {image_path}.")
        else:
            # Establecer la imagen redimensionada en el label
            self.label.setPixmap(pixmap)

    def load_and_resize_image(self, image_path):
        # Usar OpenCV para cargar la imagen
        image = cv2.imread(image_path)
        if image is None:
            return QPixmap()

        # Redimensionar la imagen al tamaño de pitch.png
        resized_image = cv2.resize(image, (self.original_size.width(), self.original_size.height()),
                                   interpolation=cv2.INTER_AREA)

        # Convertir la imagen redimensionada de OpenCV a QImage
        height, width, channel = resized_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # Convertir QImage a QPixmap
        return QPixmap.fromImage(q_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
