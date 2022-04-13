from queries import get_stock_data
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, Signal

class StockData(QAbstractListModel):

    update_logo = Signal(bytes)
    update_country_icon = Signal(bytes)
    update_news = Signal(list)
    update_value = Signal(float, float, float)
    update_profitability = Signal(float, float, float)
    update_growth = Signal(float, float, float)

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
            self.update_value.emit(
                (self.stockdata[20]["e/p"][-1]),
                self.stockdata[20]["b/m"][-1],
                self.stockdata[20]["s/p"][-1]
            )
            self.update_profitability.emit(
                self.stockdata[20]["roe ttm"][-1],
                self.stockdata[20]["roa ttm"][-1],
                self.stockdata[20]["net margin ttm"][-1]
            )
            self.update_growth.emit(
                self.stockdata[20]["revenue growth ttm"][-1],
                self.stockdata[20]["net income growth ttm"][-1],
                self.stockdata[20]["reinvestment rate ttm"][-1]
            )
            return True
        return False