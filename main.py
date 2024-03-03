"""
We will build an excel clone that can display spreadsheets and import csv files
"""



import sys
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow


app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()

