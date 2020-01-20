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

        # “数据总览”页
        self.displayLotteryData()
        self.updateData.clicked.connect(self.updateLotteryData)
        self.exportAllData.clicked.connect(self.exportLotteryData)

        # “号码出现次数”页
        self.displayPerNumberCount()
        self.exportPerNumberCount.clicked.connect(
            self.exportPerNumberCountData)

        # “奇偶”页
        self.displayOddEvenTable()
        self.exportOddEven.clicked.connect(self.exportOddEvenData)
        self.oddEvenBarChartLimit.setText(str(phaseNoLimit))
        self.oddEvenPieChartLimit.setText(str(phaseNoLimit))
        self.repaintOddEvenBarChartButton.clicked.connect(
            self.repaintOddEvenBarChart)
        self.repaintOddEvenPieChartButton.clicked.connect(
            self.repaintOddEvenPieChart)
        self.renderOddEvenBarChart(phaseNoLimit)
        self.renderOddEvenPieChart(phaseNoLimit)

        # “大小”页
        self.displayBigSmallTable()
        self.exportBigSmall.clicked.connect(self.exportBigSmallData)
        self.bigSmallBarChartLimit.setText(str(phaseNoLimit))
        self.bigSmallPieChartLimit.setText(str(phaseNoLimit))
        self.repaintBigSmallBarChartButton.clicked.connect(
            self.repaintBigSmallBarChart)
        self.repaintBigSmallPieChartButton.clicked.connect(
            self.repaintBigSmallPieChart)
        self.renderBigSmallBarChart(phaseNoLimit)
        self.renderBigSmallPieChart(phaseNoLimit)

        # “阴阳”页
        self.displayYinYangTable()
        self.exportYinYang.clicked.connect(self.exportYinYangData)
        self.yinYangBarChartLimit.setText(str(phaseNoLimit))
        self.yinYangPieChartLimit.setText(str(phaseNoLimit))
        self.repaintYinYangBarChartButton.clicked.connect(
            self.repaintYinYangBarChart)
        self.repaintYinYangPieChartButton.clicked.connect(
            self.repaintYinYangPieChart)
        self.renderYinYangBarChart(phaseNoLimit)
        self.renderYinYangPieChart(phaseNoLimit)

        # “质合”页
        self.displayPrimeCompositeTable()
        self.exportPrimeComposite.clicked.connect(
            self.exportPrimeCompositeData)
        self.primeCompositeBarChartLimit.setText(str(phaseNoLimit))
        self.primeCompositePieChartLimit.setText(str(phaseNoLimit))
        self.repaintPrimeCompositeBarChartButton.clicked.connect(
            self.repaintPrimeCompositeBarChart)
        self.repaintPrimeCompositePieChartButton.clicked.connect(
            self.repaintPrimeCompositePieChart)
        self.renderPrimeCompositeBarChart(phaseNoLimit)
        self.renderPrimeCompositePieChart(phaseNoLimit)

        # “和值”页
        self.displayCalcSumTable()
        self.exportCalcSum.clicked.connect(self.exportCalcSumData)
        self.calcSumBarChartLimit.setText(str(phaseNoLimit))
        self.calcSumPieChartLimit.setText(str(phaseNoLimit))
        self.repaintCalcSumBarChartButton.clicked.connect(
            self.repaintCalcSumBarChart)
        self.repaintCalcSumPieChartButton.clicked.connect(
            self.repaintCalcSumPieChart)
        self.renderCalcSumBarChart(phaseNoLimit)
        self.renderCalcSumPieChart(phaseNoLimit)

        # “012路”页
        self.displayCalc012Table()
        self.exportCalc012.clicked.connect(self.exportCalc012Data)
        self.calc012BarChartLimit.setText(str(phaseNoLimit))
        self.calc012PieChartLimit.setText(str(phaseNoLimit))
        self.repaintCalc012BarChartButton.clicked.connect(
            self.repaintCalc012BarChart)
        self.repaintCalc012PieChartButton.clicked.connect(
            self.repaintCalc012PieChart)
        self.renderCalc012BarChart(phaseNoLimit)
        self.renderCalc012PieChart(phaseNoLimit)

        # “跨度”页
        self.displayCalcSpanTable()
        self.exportCalcSpan.clicked.connect(self.exportCalcSpanData)
        self.calcSpanBarChartLimit.setText(str(phaseNoLimit))
        self.calcSpanPieChartLimit.setText(str(phaseNoLimit))
        self.repaintCalcSpanBarChartButton.clicked.connect(
            self.repaintCalcSpanBarChart)
        self.repaintCalcSpanPieChartButton.clicked.connect(
            self.repaintCalcSpanPieChart)
        self.renderCalcSpanBarChart(phaseNoLimit)
        self.renderCalcSpanPieChart(phaseNoLimit)

    def displayLotteryData(self):
        columns, allData = self.db.getWinningData()
        allData.reverse()
        rowCount = len(allData)
        colCount = len(columns)
        self.allDataTable.setRowCount(rowCount)
        self.allDataTable.setColumnCount(colCount)
        self.allDataTable.setHorizontalHeaderLabels(columns)
        self.allDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.allDataTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            for colIndex in range(colCount):
                item = QTableWidgetItem()
                if isinstance(allData[rowIndex][colIndex], str):
                    item.setText(allData[rowIndex][colIndex])
                elif isinstance(allData[rowIndex][colIndex], int):
                    item.setData(Qt.DisplayRole, allData[rowIndex][colIndex])
                else:
                    item.setText("")
                item.setTextAlignment(Qt.AlignCenter)
                self.allDataTable.setItem(rowIndex, colIndex, item)

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
        self.perNumberCountTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            for colIndex in range(colCount):
                item = QTableWidgetItem()
                if colIndex == 0:    # 第一列设为字符串类型
                    item.setText(str(perNumberCount[rowIndex][colIndex]))
                else:   # 第二列设为数值类型
                    item.setData(Qt.DisplayRole,
                                 perNumberCount[rowIndex][colIndex])
                item.setTextAlignment(Qt.AlignCenter)
                self.perNumberCountTable.setItem(rowIndex, colIndex, item)

        self.perNumberCountTableOrderType = Qt.AscendingOrder

    def exportPerNumberCountData(self):
        self.exportPerNumberCount.setEnabled(False)
        matrix = self.tableData2Matrix(self.perNumberCountTable, [1])
        tools.export2Excel(matrix, "xlsx/perNumberCount.xlsx")
        self.exportPerNumberCount.setText("导出成功")

    def displayOddEvenTable(self):
        tableHeaders = ["奇奇奇", "奇奇偶", "奇偶奇", "偶奇奇", "偶偶奇", "偶奇偶", "奇偶偶", "偶偶偶"]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.oddEvenTable.setRowCount(rowCount)
        self.oddEvenTable.setColumnCount(colCount)
        self.oddEvenTable.setHorizontalHeaderLabels(tableHeaders)
        self.oddEvenTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.oddEvenTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            numberAttr = ""
            for char in number:
                numberAttr += "偶" if int(char) % 2 == 0 else "奇"
            self.oddEvenTable.setItem(
                rowIndex, tableHeaders.index(numberAttr), item)

    def exportOddEvenData(self):
        self.exportOddEven.setEnabled(False)
        matrix = self.tableData2Matrix(self.oddEvenTable, [])
        tools.export2Excel(matrix, "xlsx/oddEven.xlsx")
        self.exportOddEven.setText("导出成功")

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
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="奇偶"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
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

    def displayBigSmallTable(self):
        tableHeaders = ["大大大", "大大小", "大小大", "小大大", "大小小", "小大小", "小小大", "小小小"]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.bigSmallTable.setRowCount(rowCount)
        self.bigSmallTable.setColumnCount(colCount)
        self.bigSmallTable.setHorizontalHeaderLabels(tableHeaders)
        self.bigSmallTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bigSmallTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            numberAttr = ""
            for char in number:
                numberAttr += "小" if int(char) <= 4 else "大"
            self.bigSmallTable.setItem(
                rowIndex, tableHeaders.index(numberAttr), item)

    def exportBigSmallData(self):
        self.exportBigSmall.setEnabled(False)
        matrix = self.tableData2Matrix(self.bigSmallTable, [])
        tools.export2Excel(matrix, "xlsx/bigSmall.xlsx")
        self.exportBigSmall.setText("导出成功")

    def repaintBigSmallBarChart(self):
        limit = int(self.bigSmallBarChartLimit.text())
        self.renderBigSmallBarChart(limit)

    def repaintBigSmallPieChart(self):
        limit = int(self.bigSmallPieChartLimit.text())
        self.renderBigSmallPieChart(limit)

    def renderBigSmallBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        bigSmall = {
            "大大大": 0, "大大小": 0, "大小大": 0,
            "小大大": 0, "大小小": 0, "小大小": 0,
            "小小大": 0, "小小小": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "小" if int(char) <= 4 else "大"
            bigSmall[key] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(bigSmall.keys()))
        barChart.add_yaxis("大小", list(bigSmall.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="大小"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/bigSmallBarChart.html")

        if not hasattr(self, "bigSmallBarChart"):    # 如果 bigSmallBarChart 不存在（即第一次渲染）
            self.bigSmallBarChart = QWebEngineView(self.bigSmallBarChartTab)
            self.bigSmallBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.bigSmallBarChart.setObjectName("bigSmallBarChart")
        self.bigSmallBarChart.load(
            QUrl("file:///" + QFileInfo("charts/bigSmallBarChart.html").absoluteFilePath()))

    def renderBigSmallPieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        bigSmall = {
            "大大大": 0, "大大小": 0, "大小大": 0,
            "小大大": 0, "大小小": 0, "小大小": 0,
            "小小大": 0, "小小小": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "小" if int(char) <= 4 else "大"
            bigSmall[key] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(bigSmall.keys(), bigSmall.values())), rosetype="radius")
        pieChart.render("charts/bigSmallPieChart.html")

        if not hasattr(self, "bigSmallPieChart"):
            self.bigSmallPieChart = QWebEngineView(self.bigSmallPieChartTab)
            self.bigSmallPieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.bigSmallPieChart.setObjectName("bigSmallPieChart")
        self.bigSmallPieChart.load(
            QUrl("file:///" + QFileInfo("charts/bigSmallPieChart.html").absoluteFilePath()))

    def displayYinYangTable(self):
        tableHeaders = ["阴阴阴", "阴阴阳", "阴阳阴", "阳阴阴", "阴阳阳", "阳阴阳", "阳阳阴", "阳阳阳"]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.yinYangTable.setRowCount(rowCount)
        self.yinYangTable.setColumnCount(colCount)
        self.yinYangTable.setHorizontalHeaderLabels(tableHeaders)
        self.yinYangTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.yinYangTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            numberAttr = ""
            for char in number:
                numberAttr += "阳" if int(char) in [1, 2, 5, 8, 9] else "阴"
            self.yinYangTable.setItem(
                rowIndex, tableHeaders.index(numberAttr), item)

    def exportYinYangData(self):
        self.exportYinYang.setEnabled(False)
        matrix = self.tableData2Matrix(self.yinYangTable, [])
        tools.export2Excel(matrix, "xlsx/yinYang.xlsx")
        self.exportYinYang.setText("导出成功")

    def repaintYinYangBarChart(self):
        limit = int(self.yinYangBarChartLimit.text())
        self.renderYinYangBarChart(limit)

    def repaintYinYangPieChart(self):
        limit = int(self.yinYangPieChartLimit.text())
        self.renderYinYangPieChart(limit)

    def renderYinYangBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        yinYang = {
            "阴阴阴": 0, "阴阴阳": 0, "阴阳阴": 0,
            "阳阴阴": 0, "阴阳阳": 0, "阳阴阳": 0,
            "阳阳阴": 0, "阳阳阳": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "阳" if int(char) in [1, 2, 5, 8, 9] else "阴"
            yinYang[key] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(yinYang.keys()))
        barChart.add_yaxis("阴阳", list(yinYang.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="阴阳"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/yinYangBarChart.html")

        if not hasattr(self, "yinYangBarChart"):    # 如果 yinYangBarChart 不存在（即第一次渲染）
            self.yinYangBarChart = QWebEngineView(self.yinYangBarChartTab)
            self.yinYangBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.yinYangBarChart.setObjectName("yinYangBarChart")
        self.yinYangBarChart.load(
            QUrl("file:///" + QFileInfo("charts/yinYangBarChart.html").absoluteFilePath()))

    def renderYinYangPieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        yinYang = {
            "阴阴阴": 0, "阴阴阳": 0, "阴阳阴": 0,
            "阳阴阴": 0, "阴阳阳": 0, "阳阴阳": 0,
            "阳阳阴": 0, "阳阳阳": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "阳" if int(char) in [1, 2, 5, 8, 9] else "阴"
            yinYang[key] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(yinYang.keys(), yinYang.values())), rosetype="radius")
        pieChart.render("charts/yinYangPieChart.html")

        if not hasattr(self, "yinYangPieChart"):
            self.yinYangPieChart = QWebEngineView(self.yinYangPieChartTab)
            self.yinYangPieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.yinYangPieChart.setObjectName("yinYangPieChart")
        self.yinYangPieChart.load(
            QUrl("file:///" + QFileInfo("charts/yinYangPieChart.html").absoluteFilePath()))

    def displayPrimeCompositeTable(self):
        tableHeaders = ["质质质", "质质合", "质合质", "合质质", "质合合", "合质合", "合合质", "合合合"]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.primeCompositeTable.setRowCount(rowCount)
        self.primeCompositeTable.setColumnCount(colCount)
        self.primeCompositeTable.setHorizontalHeaderLabels(tableHeaders)
        self.primeCompositeTable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.primeCompositeTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            numberAttr = ""
            for char in number:
                numberAttr += "质" if tools.isPrimeNumber(int(char)) else "合"
            self.primeCompositeTable.setItem(
                rowIndex, tableHeaders.index(numberAttr), item)

    def exportPrimeCompositeData(self):
        self.exportPrimeComposite.setEnabled(False)
        matrix = self.tableData2Matrix(self.primeCompositeTable, [])
        tools.export2Excel(matrix, "xlsx/primeComposite.xlsx")
        self.exportPrimeComposite.setText("导出成功")

    def repaintPrimeCompositeBarChart(self):
        limit = int(self.primeCompositeBarChartLimit.text())
        self.renderPrimeCompositeBarChart(limit)

    def repaintPrimeCompositePieChart(self):
        limit = int(self.primeCompositePieChartLimit.text())
        self.renderPrimeCompositePieChart(limit)

    def renderPrimeCompositeBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        primeComposite = {
            "质质质": 0, "质质合": 0, "质合质": 0,
            "合质质": 0, "质合合": 0, "合质合": 0,
            "合合质": 0, "合合合": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "质" if tools.isPrimeNumber(int(char)) else "合"
            primeComposite[key] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(primeComposite.keys()))
        barChart.add_yaxis("质合", list(primeComposite.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="质合"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/primeCompositeBarChart.html")

        # 如果 primeCompositeBarChart 不存在（即第一次渲染）
        if not hasattr(self, "primeCompositeBarChart"):
            self.primeCompositeBarChart = QWebEngineView(
                self.primeCompositeBarChartTab)
            self.primeCompositeBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.primeCompositeBarChart.setObjectName("primeCompositeBarChart")
        self.primeCompositeBarChart.load(
            QUrl("file:///" + QFileInfo("charts/primeCompositeBarChart.html").absoluteFilePath()))

    def renderPrimeCompositePieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        primeComposite = {
            "质质质": 0, "质质合": 0, "质合质": 0,
            "合质质": 0, "质合合": 0, "合质合": 0,
            "合合质": 0, "合合合": 0
        }
        for num in winningNumbers:
            key = ""
            for char in num:
                key += "质" if tools.isPrimeNumber(int(char)) else "合"
            primeComposite[key] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(primeComposite.keys(), primeComposite.values())), rosetype="radius")
        pieChart.render("charts/primeCompositePieChart.html")

        if not hasattr(self, "primeCompositePieChart"):
            self.primeCompositePieChart = QWebEngineView(
                self.primeCompositePieChartTab)
            self.primeCompositePieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.primeCompositePieChart.setObjectName("primeCompositePieChart")
        self.primeCompositePieChart.load(
            QUrl("file:///" + QFileInfo("charts/primeCompositePieChart.html").absoluteFilePath()))

    def displayCalcSumTable(self):
        tableHeaders = [str(i) for i in range(28)]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.calcSumTable.setRowCount(rowCount)
        self.calcSumTable.setColumnCount(colCount)
        self.calcSumTable.setHorizontalHeaderLabels(tableHeaders)
        self.calcSumTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.calcSumTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            numberSum = sum([int(i) for i in list(number)])
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            self.calcSumTable.setItem(rowIndex, numberSum, item)

    def exportCalcSumData(self):
        self.exportCalcSum.setEnabled(False)
        matrix = self.tableData2Matrix(self.calcSumTable, [])
        tools.export2Excel(matrix, "xlsx/calcSum.xlsx")
        self.exportCalcSum.setText("导出成功")

    def repaintCalcSumBarChart(self):
        limit = int(self.calcSumBarChartLimit.text())
        self.renderCalcSumBarChart(limit)

    def repaintCalcSumPieChart(self):
        limit = int(self.calcSumPieChartLimit.text())
        self.renderCalcSumPieChart(limit)

    def renderCalcSumBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calcSum = {str(i): 0 for i in range(28)}
        for num in winningNumbers:
            numSum = sum([int(i) for i in list(num)])
            calcSum[str(numSum)] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(calcSum.keys()))
        barChart.add_yaxis("和值", list(calcSum.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="和值"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/calcSumBarChart.html")

        if not hasattr(self, "calcSumBarChart"):    # 如果 calcSumBarChart 不存在（即第一次渲染）
            self.calcSumBarChart = QWebEngineView(self.calcSumBarChartTab)
            self.calcSumBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calcSumBarChart.setObjectName("calcSumBarChart")
        self.calcSumBarChart.load(
            QUrl("file:///" + QFileInfo("charts/calcSumBarChart.html").absoluteFilePath()))

    def renderCalcSumPieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calcSum = {str(i): 0 for i in range(28)}
        for num in winningNumbers:
            numSum = sum([int(i) for i in list(num)])
            calcSum[str(numSum)] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(calcSum.keys(), calcSum.values())), rosetype="radius")
        pieChart.render("charts/calcSumPieChart.html")

        if not hasattr(self, "calcSumPieChart"):
            self.calcSumPieChart = QWebEngineView(self.calcSumPieChartTab)
            self.calcSumPieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calcSumPieChart.setObjectName("calcSumPieChart")
        self.calcSumPieChart.load(
            QUrl("file:///" + QFileInfo("charts/calcSumPieChart.html").absoluteFilePath()))

    def displayCalc012Table(self):
        tableHeaders = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    tableHeaders.append(str(i) + str(j) + str(k))
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.calc012Table.setRowCount(rowCount)
        self.calc012Table.setColumnCount(colCount)
        self.calc012Table.setHorizontalHeaderLabels(tableHeaders)
        self.calc012Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.calc012Table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            numberAttr = ""
            for char in number:
                numberAttr += str(int(char) % 3)
            self.calc012Table.setItem(
                rowIndex, tableHeaders.index(numberAttr), item)

    def exportCalc012Data(self):
        self.exportCalc012.setEnabled(False)
        matrix = self.tableData2Matrix(self.calc012Table, [])
        tools.export2Excel(matrix, "xlsx/calc012.xlsx")
        self.exportCalc012.setText("导出成功")

    def repaintCalc012BarChart(self):
        limit = int(self.calc012BarChartLimit.text())
        self.renderCalc012BarChart(limit)

    def repaintCalc012PieChart(self):
        limit = int(self.calc012PieChartLimit.text())
        self.renderCalc012PieChart(limit)

    def renderCalc012BarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calc012 = {}
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    calc012[str(i) + str(j) + str(k)] = 0
        for num in winningNumbers:
            key = ""
            for char in num:
                key += str(int(char) % 3)
            calc012[key] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(calc012.keys()))
        barChart.add_yaxis("012路", list(calc012.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="012路"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/calc012BarChart.html")

        if not hasattr(self, "calc012BarChart"):    # 如果 calc012BarChart 不存在（即第一次渲染）
            self.calc012BarChart = QWebEngineView(self.calc012BarChartTab)
            self.calc012BarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calc012BarChart.setObjectName("calc012BarChart")
        self.calc012BarChart.load(
            QUrl("file:///" + QFileInfo("charts/calc012BarChart.html").absoluteFilePath()))

    def renderCalc012PieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calc012 = {}
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    calc012[str(i) + str(j) + str(k)] = 0
        for num in winningNumbers:
            key = ""
            for char in num:
                key += str(int(char) % 3)
            calc012[key] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(calc012.keys(), calc012.values())), rosetype="radius")
        pieChart.render("charts/calc012PieChart.html")

        if not hasattr(self, "calc012PieChart"):
            self.calc012PieChart = QWebEngineView(self.calc012PieChartTab)
            self.calc012PieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calc012PieChart.setObjectName("calc012PieChart")
        self.calc012PieChart.load(
            QUrl("file:///" + QFileInfo("charts/calc012PieChart.html").absoluteFilePath()))

    def displayCalcSpanTable(self):
        tableHeaders = [str(i) for i in range(10)]
        winningNumbers = self.db.getWinningNumbers(-1)
        rowCount = len(winningNumbers)
        colCount = len(tableHeaders)
        self.calcSpanTable.setRowCount(rowCount)
        self.calcSpanTable.setColumnCount(colCount)
        self.calcSpanTable.setHorizontalHeaderLabels(tableHeaders)
        self.calcSpanTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.calcSpanTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置单元格自适应列宽并等宽
        for rowIndex in range(rowCount):
            number = winningNumbers[rowIndex]
            separatedNumbers = [int(i) for i in list(number)]
            span = max(separatedNumbers) - min(separatedNumbers)
            item = QTableWidgetItem(number)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(255, 255, 0))
            self.calcSpanTable.setItem(rowIndex, span, item)

    def exportCalcSpanData(self):
        self.exportCalcSpan.setEnabled(False)
        matrix = self.tableData2Matrix(self.calcSpanTable, [])
        tools.export2Excel(matrix, "xlsx/calcSpan.xlsx")
        self.exportCalcSpan.setText("导出成功")

    def repaintCalcSpanBarChart(self):
        limit = int(self.calcSpanBarChartLimit.text())
        self.renderCalcSpanBarChart(limit)

    def repaintCalcSpanPieChart(self):
        limit = int(self.calcSpanPieChartLimit.text())
        self.renderCalcSpanPieChart(limit)

    def renderCalcSpanBarChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calcSpan = {str(i): 0 for i in range(10)}
        for num in winningNumbers:
            separatedNumbers = [int(i) for i in list(num)]
            span = max(separatedNumbers) - min(separatedNumbers)
            calcSpan[str(span)] += 1

        barChart = charts.Bar()
        barChart.width = '750px'
        barChart.height = '470px'
        barChart.add_xaxis(list(calcSpan.keys()))
        barChart.add_yaxis("跨度", list(calcSpan.values()))
        barChart.set_global_opts(
            xaxis_opts=options.AxisOpts(name="跨度"),
            yaxis_opts=options.AxisOpts(name="数量")
        )
        barChart.render("charts/calcSpanBarChart.html")

        if not hasattr(self, "calcSpanBarChart"):    # 如果 calcSpanBarChart 不存在（即第一次渲染）
            self.calcSpanBarChart = QWebEngineView(self.calcSpanBarChartTab)
            self.calcSpanBarChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calcSpanBarChart.setObjectName("calcSpanBarChart")
        self.calcSpanBarChart.load(
            QUrl("file:///" + QFileInfo("charts/calcSpanBarChart.html").absoluteFilePath()))

    def renderCalcSpanPieChart(self, limit):
        winningNumbers = self.db.getWinningNumbers(limit)
        calcSpan = {str(i): 0 for i in range(10)}
        for num in winningNumbers:
            separatedNumbers = [int(i) for i in list(num)]
            span = max(separatedNumbers) - min(separatedNumbers)
            calcSpan[str(span)] += 1

        pieChart = charts.Pie()
        pieChart.width = '750px'
        pieChart.height = '470px'
        pieChart.add(series_name="", data_pair=list(
            zip(calcSpan.keys(), calcSpan.values())), rosetype="radius")
        pieChart.render("charts/calcSpanPieChart.html")

        if not hasattr(self, "calcSpanPieChart"):
            self.calcSpanPieChart = QWebEngineView(self.calcSpanPieChartTab)
            self.calcSpanPieChart.setGeometry(QRect(-1, -1, 771, 490))
            self.calcSpanPieChart.setObjectName("calcSpanPieChart")
        self.calcSpanPieChart.load(
            QUrl("file:///" + QFileInfo("charts/calcSpanPieChart.html").absoluteFilePath()))

    # asNumber 是一个数组，存在于 asNumber 中的列索引对应的列会作为 数字 类型
    def tableData2Matrix(self, qtTable, asNumber):
        matrix = []
        rowCount = qtTable.rowCount()
        colCount = qtTable.columnCount()
        oneRow = []
        for colIndex in range(colCount):  # 将表格头放入 matrix
            oneRow.append(qtTable.horizontalHeaderItem(colIndex).text())
        matrix.append(oneRow)
        for rowIndex in range(rowCount):  # 将表格数据放入 matrix
            oneRow = []
            for colIndex in range(colCount):
                item = qtTable.item(rowIndex, colIndex)
                if item is None:
                    oneRow.append("")
                    continue
                if colIndex in asNumber:
                    oneRow.append(item.data(Qt.DisplayRole))
                else:
                    oneRow.append(item.text())
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
