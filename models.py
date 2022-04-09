from queries import get_stock_data
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, Signal

class StockData(QAbstractListModel):

    update_logo = Signal(bytes)
    update_country_icon = Signal(bytes)
    update_news = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.stockdata = ["" for _ in range(20)]

    def rowCount(self, parent):
        return len(self.stockdata)

    def data(self, index, role):
        row = index.row()
        return self.stockdata[row]
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.row() == -1:
            self.stockdata = get_stock_data(value)
            for row in range(self.rowCount(QModelIndex())):
                index = self.index(row, 0, QModelIndex())
                self.dataChanged.emit(index, index)
            self.update_logo.emit(self.stockdata[0])
            self.update_country_icon.emit(self.stockdata[8])
            self.update_news.emit(self.stockdata[19])
            return True
        return False