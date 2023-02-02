#!/usr/bin/env python

# Importa bibliotecas necessárias
import sys

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5 import QtWidgets

from orifice_plate.orifice_plate import OrificePlate

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo de placas de orifício")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(1440, 900)

        # Create widgets
        self.pipe_diameter_label = QtWidgets.QLabel("Diâmetro da tubulação (m):")
        self.pipe_diameter_input = QtWidgets.QLineEdit()
        self.orifice_diameter_label = QtWidgets.QLabel("Diâmetro do orifício (m):")
        self.orifice_diameter_input = QtWidgets.QLineEdit()
        self.differential_pressure_label = QtWidgets.QLabel("Pressão diferencial:")
        self.differential_pressure_input = QtWidgets.QLineEdit()
        self.fluid_density_label = QtWidgets.QLabel("Densidade do fluido:")
        self.fluid_density_input = QtWidgets.QLineEdit()
        self.fluid_viscosity_label = QtWidgets.QLabel("Viscosidade do fluido:")
        self.fluid_viscosity_input = QtWidgets.QLineEdit()
        self.Reynolds_label = QtWidgets.QLabel("Reynolds:")
        self.Reynolds_input = QtWidgets.QLineEdit()
        self.update_button = QtWidgets.QPushButton("Atualizar parâmetros")

        # Create dropdown menu 1
        self.dropdown_menu_1_label = QtWidgets.QLabel("Tipo de bordo")
        self.dropdown_menu_1 = QtWidgets.QComboBox()
        self.dropdown_menu_1.addItems(["Bordo reto", "Bordo redondo", "Bordo em V"])

        # Create dropdown menu 2
        self.dropdown_menu_2_label = QtWidgets.QLabel("Tipo de Tap")
        self.dropdown_menu_2 = QtWidgets.QComboBox()
        self.dropdown_menu_2.addItems(["Tap radial", "Tap de canto", "Tap radial", "Tap de tubo"])

        # Create input layout
        self.input_layout = QtWidgets.QHBoxLayout()
        self.input_layout.addWidget(self.pipe_diameter_label)
        self.input_layout.addWidget(self.pipe_diameter_input)
        self.input_layout.addWidget(self.orifice_diameter_label)
        self.input_layout.addWidget(self.orifice_diameter_input)
        self.input_layout.addWidget(self.differential_pressure_label)
        self.input_layout.addWidget(self.differential_pressure_input)
        self.input_layout.addWidget(self.fluid_density_label)
        self.input_layout.addWidget(self.fluid_density_input)
        self.input_layout.addWidget(self.fluid_viscosity_label)
        self.input_layout.addWidget(self.fluid_viscosity_input)
        self.input_layout.addWidget(self.Reynolds_label)
        self.input_layout.addWidget(self.Reynolds_input)

        # Add dropdown menus to the input layout
        self.input_layout.addWidget(self.dropdown_menu_1_label)
        self.input_layout.addWidget(self.dropdown_menu_1)
        self.input_layout.addWidget(self.dropdown_menu_2_label)
        self.input_layout.addWidget(self.dropdown_menu_2)

        self.input_layout.addStretch(1)

        # Create graphics view
        self.graphics_view_side = QtWidgets.QGraphicsView()
        self.graphics_scene_side = QtWidgets.QGraphicsScene()
        self.graphics_view_side.setScene(self.graphics_scene_side)

        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.graphics_view_side)
        self.main_layout.addWidget(self.update_button)

        # Set layout
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Connect signals
        self.update_button.clicked.connect(self.update_drawing)


    def update_drawing(self):
        index = self.dropdown_menu_1.currentIndex()
        data_edge = self.dropdown_menu_1.itemText(index)
        index = self.dropdown_menu_2.currentIndex()
        data_tap_type = self.dropdown_menu_2.itemText(index)

        data_pipe_diameter = float(self.pipe_diameter_input.text()) if self.pipe_diameter_input.text() else 0
        data_orifice_diameter = float(self.orifice_diameter_input.text()) if self.orifice_diameter_input.text() else 0
        data_differential_pressure = float(self.differential_pressure_input.text()) if self.differential_pressure_input.text() else 0
        data_fluid_density = float(self.fluid_density_input.text()) if self.fluid_density_input.text() else 0
        data_fluid_viscosity = float(self.fluid_viscosity_input.text()) if self.fluid_viscosity_input.text() else 0
        data_Reynolds = float(self.Reynolds_input.text()) if self.Reynolds_input.text() else 0

        self.graphics_scene_side.clear()

        figure = Figure()
        axes = figure.gca()
        axes.set_title("Curva de vazão por pressão diferencial")
        x = np.linspace(data_differential_pressure / 1000.0, data_differential_pressure * 10.0)
        y = np.linspace(data_differential_pressure / 1000.0, data_differential_pressure * 10.0)
        
        plate = OrificePlate(
        pipe_diameter=data_pipe_diameter, 
        orifice_diameter=data_orifice_diameter, 
        differential_pressure=data_differential_pressure, 
        fluid_density=data_fluid_density, 
        fluid_viscosity=data_fluid_viscosity, 
        tap_type=data_tap_type, 
        Reynolds=data_Reynolds, 
        edge_type=data_edge)

        for index in range(x.size):
            y[index] = plate.pipe_flow_rate(x[index])

        axes.plot(y, x, "-k", label="Curva de vazão")
        axes.legend()
        axes.grid(True)

        canvas = FigureCanvas(figure)
        proxy_widget = self.graphics_scene_side.addWidget(canvas)


        self.graphics_view_side.show()