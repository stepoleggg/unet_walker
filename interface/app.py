import sys  

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from interface.ui_template import Ui_mainWindow
from interface.dialog_ui_template import Ui_Dialog
import train
import read_svo
import predict
from config import data_dir, db_name, svo_dir, update_lap_bush
from typing import List
from CapturedText import captured
import time
import traceback
import shutil
from pathlib import PurePath
from interface.TableModel import TableModel

from svo_file import Svo_file
from SVODao import Svo_DB
from analyzer import render_report

class App(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # init var
        self.svo_files: List[Svo_file] = []
        # init func
        self.choseFileButton.clicked.connect(self.file_dialog)
        self.predictButton.clicked.connect(self.predict)
        self.getDataButton.clicked.connect(self.get_data)
        self.clearButton.clicked.connect(self.clear_table)
        self.analyzeButton.clicked.connect(self.analyze)
        self.editButton.clicked.connect(self.dialog)
        # init list view
        #self.add_data_to_list_view("Выберите SVO файл")
        # init multitrading 
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # init db 
        self.update_table()
        for svo in Svo_DB.get_all_svo():
            print(svo)
            svo.get_data = True
            Svo_DB.update_svo(svo)

    def dialog(self):
        self.dia = Dialog(self)
        self.dia.show()


    def clear_table(self):
        self.svo_files = []
        self.update_table()
        self.listWidget.clear()
        
    def analyze(self):
        worker = Worker(self._analyze)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)  

    def _analyze(self, progress_callback):
        if self.current_svo_error():
            for file in self.svo_files:
                if not file.get_data:
                    if read_svo.read_svo(file.svo_path, progress_callback) == "ok":
                       file.get_data = True
                       Svo_DB.update_svo(file)
                       self.update_table()
                    else:
                        continue
                if not file.predict:
                    if predict.predict(file.svo_dir_name, progress_callback) == "ok":
                        file.predict = True
                        Svo_DB.update_svo(file)
                        self.update_table()
            self.add_data_to_list_view(f"Создание отчета для {file.file_name}")
            out = render_report(file.svo_dir_name)
            self.add_data_to_list_view(f"Отчет создан и сохранен {out}")
        return "ok"

    def update_table(self):
        data = []
        for svo_file in self.svo_files:
            data.append(svo_file.get_data_for_insert())
        if not data:
            data = [["", "", "", "", ""]]
        self.tableModel = TableModel(data)
        self.tableView.setModel(self.tableModel)


    def progress_fn(self, n):
        self.add_data_to_list_view(n)
 
    def print_output(self, s):
        print(s)
        
    def thread_complete(self):
        print("THREAD COMPLETE!")

    def file_dialog(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open SVO files', None, "Svo (*.svo)")[0]
        for svo in fname:
            self.open_svo(svo)
            """
            worker = Worker(self.open_svo, svo) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker) 
            """

     
    def predict(self):
        worker = Worker(self._predict)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)    

    def _predict(self, progress_callback):
        if self.current_svo_error():
            for file in self.svo_files:
                if not file.get_data:
                    if read_svo.read_svo(file.svo_path, progress_callback) == "ok":
                       file.get_data = True
                       Svo_DB.update_svo(file)
                       self.update_table()
                    else:
                        continue
                if predict.predict(file.svo_dir_name, progress_callback) == "ok":
                    file.predict = True
                    Svo_DB.update_svo(file)
                    self.update_table()
        return "ok"

    def get_data(self):
        if self.current_svo_error():
            worker = Worker(self._get_data) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)
    
    def _get_data(self, progress_callback):
        for file in self.svo_files:
            if not file.get_data:
                if read_svo.read_svo(file.svo_path, progress_callback) == "ok":
                    file.get_data = True
                    Svo_DB.update_svo(file)
                    self.update_table()
        return "ok"
 
    def current_svo_error(self) -> bool:
        if not self.svo_files:
            self.show_error_widget("SVO файл не выбран", "Выберите SVO файл", "SVO file not found")
            return False
        return True

    def open_svo(self, path: str, progress_callback = None):
        if path == "":
            return
        if not path.endswith(".svo"):
            self.show_error_widget("Ошибка при чтении SVO файла", f"{path} не имеет расширение SVO", "Error SVO read")
            return
        else:
            self.show_info_widget("SVO файл добавлен", f"{path}")
        
        svo = Svo_DB.get_svo_by_name(Svo_file(path))
        if not svo:
            if PurePath(path).parent != PurePath(svo_dir):
                shutil.copy(path, svo_dir)
            svo_file = Svo_file(path)
            self.svo_files.append(svo_file)
            self.add_data_to_list_view(f"{svo_file.svo_path}")
            Svo_DB.insert_svo(svo_file)
        else:
            self.svo_files.append(svo)
            self.add_data_to_list_view(f"{svo.svo_path}")
        self.update_table()
        return "ok"
       

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

class Dialog(QMainWindow, Ui_Dialog):
    def __init__(self, app: App):
        super().__init__()
        self.setupUi(self)
        self.app = app

    def accept(self):
        if self.change_config() == "ok":
            self.destroy()
    def reject(self):
        self.destroy()

    def change_config(self):
        try:
            update_lap_bush(float(self.lineEdit.text()), float(self.lineEdit_2.text()))
        except Exception as e:
            self.app.show_error_widget("Неприемлемое значение")
            print(e)
            return
        return "ok"


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App() 
    window.show()  
    app.exec_()


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(object)
    result = pyqtSignal(object)
    progress = pyqtSignal(object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done 

if __name__ == '__main__':  
    main()