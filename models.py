from queries import get_stock_data
import pandas as pd
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt, Signal

class StockData(QAbstractListModel):

    update_logo = Signal(bytes)
    update_country_icon = Signal(bytes)
    update_news = Signal(list)
    update_value_box = Signal(float, float, float)
    update_profitability_box = Signal(float, float, float)
    update_growth_box = Signal(float, float, float)
    update_fundamental_view = Signal(pd.Series, str)
    update_prices = Signal(pd.Series)

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
            self.update_value_box.emit(
                (self.stockdata[20]["e/p"].iloc[-1]),
                self.stockdata[20]["b/m"].iloc[-1],
                self.stockdata[20]["s/p"].iloc[-1]
            )
            self.update_profitability_box.emit(
                self.stockdata[20]["roe ttm"].iloc[-1],
                self.stockdata[20]["roa ttm"].iloc[-1],
                self.stockdata[20]["net margin ttm"].iloc[-1]
            )
            self.update_growth_box.emit(
                self.stockdata[20]["revenue growth ttm"].iloc[-1],
                self.stockdata[20]["net income growth ttm"].iloc[-1],
                self.stockdata[20]["reinvestment rate ttm"].iloc[-1]
            )
            self.update_fundamental_view.emit(self.stockdata[21]["revenue ttm"], "Revenue")
            self.update_prices.emit(self.stockdata[20]["close"])
            return True
        return False