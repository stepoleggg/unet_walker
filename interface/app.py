import sys  
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QMessageBox, QErrorMessage)
from PyQt5.QtGui import QIcon
from interface.ui_template import Ui_mainWindow
import train
import read_svo
import predict
from config import data_dir, db_name
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from svo_file import Svo_file

class App(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # init var
        self.svo_file: Svo_file
        # init func
        self.choseFileButton.clicked.connect(self.file_dialog)
        self.predictButton.clicked.connect(self.predict)
        self.trainButton.clicked.connect(self.train)
        self.getDataButton.clicked.connect(self.get_data)
        # init list view
        #self.add_data_to_list_view("Выберите SVO файл")


    def file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open SVO file')[0]
        self.open_svo(fname)
    
    def train(self):
        if self.current_svo_error():
            train.train()

    def predict(self):
        print(data_dir)
        if self.current_svo_error():
            predict.predict(self.svo_file.svo_path)

    def get_data(self):
        if self.current_svo_error():
            read_svo.read_svo(self.svo_file.svo_path)

    def current_svo_error(self) -> bool:
        if self.svo_file is None:
            self.show_error_widget("SVO файл не выбран", "Выберите SVO файл", "SVO file not found")
            return False
        return True

    def open_svo(self, path: str):
        if path == "":
            return
        if not path.endswith(".svo"):
            self.show_error_widget("Ошибка при чтении SVO файла", f"{path} не имеет расширение SVO", "Error SVO read")
            return
        else:
            self.show_info_widget("SVO файл добавлен", f"{path}")
        self.svo_file = Svo_file(path)
        self.add_data_to_list_view(f"{path}")
        

    def add_data_to_list_view(self, data):
        self.listWidget.addItem(data)

    def show_error_widget(self, text, more_info="", title="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(more_info)
        msg.setWindowTitle(title)
        msg.exec()

    def show_info_widget(self, text, more_info="", title="Info"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText(more_info)
        msg.setWindowTitle(title)
        msg.exec()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App() 
    window.show()  
    app.exec_() 

if __name__ == '__main__':  
    main()