# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime, timedelta
from pyecharts import charts, options
from model import Database
from crawler import Crawler
import sys
import os
import mainWindow
import tools


class MyMainWindow(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, arg=None):
        super(MyMainWindow, self).__init__(arg)
        self.setupUi(self)
        self.db = Database()
        phaseNoLimit = 100

        self.displayLotteryData()
        self.updateData.clicked.connect(self.updateLotteryData)
        self.exportAllData.clicked.connect(self.exportLotteryData)

        self.displayPerNumberCount()
        self.exportPerNumberCount.clicked.connect(
            self.exportPerNumberCountData)

        # self.displayOddEvenTable()
        self.oddEvenBarChartLimit.setText(str(phaseNoLimit))
        self.oddEvenPieChartLimit.setText(str(phaseNoLimit))
        self.repaintOddEvenBarChartButton.clicked.connect(self.repaintOddEvenBarChart)
        self.repaintOddEvenPieChartButton.clicked.connect(self.repaintOddEvenPieChart)
        self.renderOddEvenBarChart(phaseNoLimit)
        self.renderOddEvenPieChart(phaseNoLimit)

    def displayLotteryData(self):
        columns, allData = self.db.getWinningData()
        allData.reverse()
        rowCount = len(allData)
        colCount = len(columns)
        self.allDataTable.setRowCount(rowCount)
        self.allDataTable.setColumnCount(colCount)
        self.allDataTable.setHorizontalHeaderLabels(columns)
        self.allDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for row in range(rowCount):
            for col in range(colCount):
                item = QTableWidgetItem()
                if isinstance(allData[row][col], str):
                    item.setText(allData[row][col])
                elif isinstance(allData[row][col], int):
                    item.setData(Qt.DisplayRole, allData[row][col])
                else:
                    item.setText("")
                item.setTextAlignment(Qt.AlignCenter)
                self.allDataTable.setItem(row, col, item)

    def updateLotteryData(self):
        self.updateData.setEnabled(False)

        latestDateStr = self.db.getLatestDate()
        startDate = datetime.strptime(
            latestDateStr, "%Y-%m-%d") + timedelta(days=1)
        startDateStr = startDate.strftime("%Y-%m-%d")
        now = datetime.now()
        if now.hour >= 21 and now.minute >= 30:  # 福彩3D 在每日 21:15 开奖，保险起见，使用 21:30 判断是否已开奖
            endDate = now
        else:
            endDate = now - timedelta(days=1)
        endDateStr = endDate.strftime("%Y-%m-%d")
        cwl = Crawler()
        newData = cwl.getLotteryData(startDateStr, endDateStr)
        for item in newData:
            self.db.insertItem(item)

        self.displayLotteryData()

    def exportLotteryData(self):
        self.exportAllData.setEnabled(False)
        matrix = self.tableData2Matrix(self.allDataTable, [2, 3, 4])
        tools.export2Excel(matrix, "xlsx/allData.xlsx")
        self.exportAllData.setText("导出成功")

    def displayPerNumberCount(self):
        columns, perNumberCount = self.db.getPerNumberCount()
        rowCount = len(perNumberCount)
        colCount = len(columns)
        self.perNumberCountTable.setRowCount(rowCount)
        self.perNumberCountTable.setColumnCount(colCount)
        self.perNumberCountTable.setHorizontalHeaderLabels(columns)
        self.perNumberCountTable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        for row in range(rowCount):
            for col in range(colCount):
                item = QTableWidgetItem()
                if col == 0:    # 第一列设为字符串类型
                    item.setText(str(perNumberCount[row][col]))
                else:   # 第二列设为数值类型
                    item.setData(Qt.DisplayRole, perNumberCount[row][col])
                item.setTextAlignment(Qt.AlignCenter)
                self.perNumberCountTable.setItem(row, col, item)

        self.perNumberCountTableOrderType = Qt.AscendingOrder

    def exportPerNumberCountData(self):
        self.exportPerNumberCount.setEnabled(False)
        matrix = self.tableData2Matrix(self.perNumberCountTable, [1])
        tools.export2Excel(matrix, "xlsx/perNumberCount.xlsx")
        self.exportPerNumberCount.setText("导出成功")

    def repaintOddEvenBarChart(self):
        limit = int(self.oddEvenBarChartLimit.text())
        self.renderOddEvenBarChart(limit)

    def repaintOddEvenPieChart(self):
        limit = int(self.oddEvenPieChartLimit.text())
        self.renderOddEvenPieChart(limit)

    def renderOddEvenBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        oddEven = {
            "奇奇奇": 0, "奇奇偶": 0, "奇偶奇": 0,
            "偶奇奇": 0, "偶偶奇": 0, "偶奇偶": 0,
            "奇偶偶": 0, "偶偶偶": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "偶" if int(char) % 2 == 0 else "奇"
            oddEven[key] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(oddEven.keys()))
        barChart.add_yaxis("奇偶", list(oddEven.values()))
        barChart.render("charts/oddEvenBarChart.html")

        if not hasattr(self, "oddEvenBarChart"):    # 如果 oddEvenBarChart 不存在（即第一次渲染）
            self.oddEvenBarChart = QWebEngineView(self.oddEvenBarChartTab)
            self.oddEvenBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.oddEvenBarChart.setObjectName("oddEvenBarChart")
        self.oddEvenBarChart.load(
            QUrl("file:///" + QFileInfo("charts/oddEvenBarChart.html").absoluteFilePath()))

    def renderOddEvenPieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        oddEven = {
            "奇奇奇": 0, "奇奇偶": 0, "奇偶奇": 0,
            "偶奇奇": 0, "偶偶奇": 0, "偶奇偶": 0,
            "奇偶偶": 0, "偶偶偶": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "偶" if int(char) % 2 == 0 else "奇"
            oddEven[key] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(oddEven.keys(), oddEven.values())), rosetype="radius")
        pieChart.render("charts/oddEvenPieChart.html")

        if not hasattr(self, "oddEvenPieChart"):
            self.oddEvenPieChart = QWebEngineView(self.oddEvenPieChartTab)
            self.oddEvenPieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.oddEvenPieChart.setObjectName("oddEvenPieChart")
        self.oddEvenPieChart.load(
            QUrl("file:///" + QFileInfo("charts/oddEvenPieChart.html").absoluteFilePath()))

    # asNumber 是一个数组，存在于 asNumber 中的列索引对应的列会作为 数字 类型
    def tableData2Matrix(self, qtTable, asNumber):
        matrix = []
        rowCount = qtTable.rowCount()
        colCount = qtTable.columnCount()
        oneRow = []
        for col in range(colCount):  # 将表格头放入 matrix
            oneRow.append(qtTable.horizontalHeaderItem(col).text())
        matrix.append(oneRow)
        for row in range(rowCount):  # 将表格数据放入 matrix
            oneRow = []
            for col in range(colCount):
                if col in asNumber:
                    oneRow.append(qtTable.item(row, col).data(Qt.DisplayRole))
                else:
                    oneRow.append(qtTable.item(row, col).text())
            matrix.append(oneRow)
        return matrix


if __name__ == "__main__":
    if not os.path.exists("xlsx"):
        os.mkdir("xlsx")
    if not os.path.exists("charts"):
        os.mkdir("charts")
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
