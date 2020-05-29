import sys  
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QMessageBox, QErrorMessage)
from PyQt5.QtGui import QIcon
import ui_template

class App(QtWidgets.QMainWindow, ui_template.Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # init var
        self.svo_file = None
        # init func
        self.choseFileButton.clicked.connect(self.file_dialog)
        self.predictButton.clicked.connect(self.predict)
        self.trainButton.clicked.connect(self.train)
        self.getDataButton.clicked.connect(self.get_data)
        # init list view
        self.add_data_to_list_view("Выберите SVO файл")


    def file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open svo file')[0]
        self.open_svo(fname)
    
    def train(self):
        self.current_svo_error()

    def predict(self):
        self.current_svo_error()

    def get_data(self):
        self.current_svo_error()

    def current_svo_error(self):
        if self.svo_file is None:
            self.show_error_widget("svo файл не выбран", "Выберите svo файл", "svo file not found")

    def open_svo(self, path: str):
        if path == "":
            return
        if not path.endswith(".svo"):
            self.show_error_widget("Ошибка при чтении svo файла", f"{path} не имеет расширение svo", "Error svo read")
            return
        else:
            self.show_info_widget("svo файл выбран", f"{path}")
        self.svo_file = path
        self.add_data_to_list_view(f"Текущий svo фыйл {path}")
        

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