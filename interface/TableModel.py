from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from datetime import datetime

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_labels = ['Имя файла', 'Дата загрузки', 'Данные получены', 'Данные обработаны', 'Проанализированно']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]

            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, bool):
                return str(value)

            if isinstance(value, str):
                return value

            return value

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])