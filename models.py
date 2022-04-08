from queries import get_company_profile
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, Signal

class StockData(QAbstractListModel):

    def __init__(self) -> None:
        super().__init__()
        self.stockdata = ["" for _ in range(20)]

    def rowCount(self, parent):
        return len(self.stockdata)

    def data(self, index, role):
        row = index.row()
        return self.stockdata[row]
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.row() == 0:
            self.stockdata = get_company_profile(value)
            for row in range(self.rowCount(QModelIndex())):
                index = self.index(row, 0, QModelIndex())
                self.dataChanged.emit(index, index)
            return True
        return False