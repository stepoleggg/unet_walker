import sys  

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from interface.ui_template import Ui_mainWindow
import train
import read_svo
import predict
from config import data_dir, db_name
from typing import List
from CapturedText import captured
import time
import traceback

from svo_file import Svo_file

class App(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # init var
        self.svo_files: List[Svo_file] = []
        # init func
        self.choseFileButton.clicked.connect(self.file_dialog)
        self.predictButton.clicked.connect(self.predict)
        self.trainButton.clicked.connect(self.train)
        self.getDataButton.clicked.connect(self.get_data)
        # init list view
        #self.add_data_to_list_view("Выберите SVO файл")
        # init multitrading 
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def progress_fn(self, n):
        self.add_data_to_list_view(str(n))
 
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

     
    def train(self):
        if self.current_svo_error():
            train.train()

    def predict(self):
        if self.current_svo_error():
            predict.predict(self.svo_file.svo_path)

    def get_data(self):
        if self.current_svo_error():
            worker = Worker(self._get_data) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)
    
    def _get_data(self, progress_callback):
        with captured(progress_callback) as c:
            read_svo.read_svo(self.svo_files[0].svo_path)
 
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
        svo_file = Svo_file(path)
        self.svo_files.append(svo_file)
        self.add_data_to_list_view(f"{path}")
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