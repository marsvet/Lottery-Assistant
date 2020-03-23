# -*-coding:utf-8-*-
import sqlite3


class Database:
    def __init__(self):
        self.db = sqlite3.connect(
            "../database.sqlite3", check_same_thread=False)  # check_same_thread=False : 允许 sqlite 数据库被多个线程访问

    def getWinningData(self):  # 从“中奖数据”视图中获取所有中奖数据
        cursor = self.db.cursor()
        cursor.execute("select * from 中奖数据")
        winningData = cursor.fetchall()
        # columns = [item[0] for item in cursor.description]    # 获取表头信息
        cursor.close()
        # return columns, winningData
        return winningData

    def getLatestDate(self):  # 获取数据库中最新数据的日期
        cursor = self.db.cursor()
        cursor.execute("select max(开奖日期) from lottery_data")
        latestDate = cursor.fetchone()[0]
        cursor.close()
        return latestDate

    def insertItem(self, item):
        cursor = self.db.cursor()
        cursor.execute(
            "insert into lottery_data values('%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % tuple(item))
        self.db.commit()
        cursor.close()

    def __del__(self):
        self.db.close()
