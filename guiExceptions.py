
from PySide6.QtWidgets import *

class NoFileFound(Exception):
    pass















#Critical        
def button_clicked_critical(self):
    ret = QMessageBox.critical(self,"Message Title",
                                    "Critical Message!",
                                    QMessageBox.Ok | QMessageBox.Cancel)
    if ret == QMessageBox.Ok : 
        print("User chose OK")
    else : 
        print ("User chose Cancel")

#Question
def button_clicked_question(self):
    ret = QMessageBox.question(self,"Message Title",
                                    "Asking a question?",
                                    QMessageBox.Ok | QMessageBox.Cancel)
    if ret == QMessageBox.Ok : 
        print("User chose OK")
    else : 
        print ("User chose Cancel")

#Information
def button_clicked_information(self):
    ret = QMessageBox.information(self,"Message Title",
                                    "Some information",
                                    QMessageBox.Ok | QMessageBox.Cancel)
    if ret == QMessageBox.Ok : 
        print("User chose OK")
    else : 
        print ("User chose Cancel")

#Warning
def button_clicked_warning(self):
    ret = QMessageBox.warning(self,"Message Title",
                                    "Some Warning",
                                    QMessageBox.Ok | QMessageBox.Cancel)
    if ret == QMessageBox.Ok : 
        print("User chose OK")
    else : 
        print ("User chose Cancel")

#About
def button_clicked_about(self):
    ret = QMessageBox.about(self,"Message Title",
                                    "Some about message")
    if ret == QMessageBox.Ok : 
        print("User chose OK")
    else : 
        print ("User chose Cancel")