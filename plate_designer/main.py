#!/usr/bin/env python

# Importa bibliotecas necessárias
import sys

from ui.ui import MainWindow

from PyQt5.QtWidgets import (
    QApplication,
)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
