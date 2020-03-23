# -*-coding:utf-8-*-
#
# 定时任务
#
from app import crawler, db
from datetime import datetime, timedelta


def updateDB():
    latestDateStr = db.getLatestDate()
    startDate = datetime.strptime(
        latestDateStr, "%Y-%m-%d") + timedelta(days=1)
    startDateStr = startDate.strftime("%Y-%m-%d")
    endDateStr = datetime.now().strftime("%Y-%m-%d")
    newData = crawler.getLotteryData(startDateStr, endDateStr)
    for item in newData:
        db.insertItem(item)
