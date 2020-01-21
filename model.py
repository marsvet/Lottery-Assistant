import sqlite3


class Database:
    def __init__(self):
        self.db = sqlite3.connect("database.sqlite3")

    def getAllData(self):   # 获取所有数据
        cursor = self.db.cursor()
        cursor.execute("select * from lottery_data")
        allData = cursor.fetchall()
        columns = [item[0] for item in cursor.description]
        cursor.close()
        return columns, allData

    def getWinningData(self):   # 从“中奖数据”视图中获取所有中奖数据
        cursor = self.db.cursor()
        cursor.execute("select * from 中奖数据")
        winningData = cursor.fetchall()
        columns = [item[0] for item in cursor.description]
        cursor.close()
        return columns, winningData

    def getWinningNumbers(self, limit=-1):  # 获取最近 limit 期的中奖号码。若 limit 为负数，表示获取全部
        cursor = self.db.cursor()
        if limit < 0:
            sql = "select 中奖号码 from 中奖号码"
        else:
            sql = "select 中奖号码 from 中奖号码 limit %d" % limit
        cursor.execute(sql)
        winningNumbers = cursor.fetchall()
        winningNumbers = [item[0] for item in winningNumbers]
        cursor.close()
        return winningNumbers

    def getPerNumberCount(self, limit=-1):  # 获取最近 limit 期中，每个号码出现的次数
        winningNumbers = self.getWinningNumbers(limit)
        counter = {}
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    counter[str(i) + str(j) + str(k)] = 0
        for num in winningNumbers:
            counter[num] += 1
        columns = ["中奖号码", "次数"]
        perNumberCount = list(zip(counter.keys(), counter.values()))
        return columns, perNumberCount

    def getLatestDate(self):    # 获取数据库中最新数据的日期
        cursor = self.db.cursor()
        cursor.execute("select max(开奖日期) from lottery_data")
        latestDate = cursor.fetchone()[0]
        cursor.close()
        return latestDate

    def insertItem(self, item):
        cursor = self.db.cursor()
        cursor.execute("insert into lottery_data values('%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % tuple(item))
        self.db.commit()
        cursor.close()

    def __del__(self):
        self.db.close()
