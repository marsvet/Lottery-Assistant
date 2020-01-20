from openpyxl import Workbook


def export2Excel(matrix, filePath):  # 参数是一个矩阵 和 文件保存路径
    wb = Workbook()
    ws = wb.active
    for row in range(1, len(matrix) + 1):
        for col in range(1, len(matrix[row - 1]) + 1):
            ws.cell(row, col, matrix[row - 1][col - 1])
    wb.save(filePath)

def isPrimeNumber(num): # 判断 num 是否为质数。这里把 0 看做合数，1 看做质数
    if not isinstance(num, int) or num < 0:
        return None
    if num == 0:
        return False
    if num == 1:
        return True
    for i in range(2, num):
        if num % i == 0:
            return False
    return True
