# -*-coding:utf-8-*-
from openpyxl import Workbook


def export2Excel(matrix, filePath):  # 参数是一个矩阵 和 文件保存路径
    wb = Workbook()
    ws = wb.active
    for row in range(1, len(matrix) + 1):
        for col in range(1, len(matrix[row - 1]) + 1):
            ws.cell(row, col, matrix[row - 1][col - 1])
    wb.save(filePath)
