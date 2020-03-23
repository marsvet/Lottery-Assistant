import requests as req
import time
import json


class Crawler:
    def __init__(self):
        self.headers = {    # 基本的头数据
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }

    def getLotteryData(self, startDate, endDate):
        headers = self.headers.copy()
        headers.update({
            "referer": "http://www.cwl.gov.cn/kjxx/fc3d/kjgg/"
        })
        url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&dayStart=%s&dayEnd=%s&pageNo=%d"
        rsp = req.get(url % (startDate, endDate, 1), headers=headers)
        pageCount = int(json.loads(rsp.text)["pageCount"])
        if pageCount == 0:
            return []
        page1Data = json.loads(rsp.text)["result"]
        page1Data.reverse()
        allData = []
        clearedData = []
        for i in range(pageCount, 1, -1):
            time.sleep(5)  # 睡 5s，防止被封
            rsp = req.get(url % (startDate, endDate, i), headers=headers)
            data = json.loads(rsp.text)["result"]
            data.reverse()
            allData.extend(data)
        allData.extend(page1Data)
        for item in allData:
            phaseNo = item["code"]
            dateAndWeek = item["date"]
            date = dateAndWeek[:10]
            week = dateAndWeek[11]
            winNumber = item["red"].split(',')
            totalMoney = item["sales"] if item["sales"] != "" else "null"
            danxuanNum = item["prizegrades"][0]["typenum"] if item["prizegrades"][0]["typenum"] != "" else "null"
            danxuanMoney = item["prizegrades"][0]["typemoney"] if item["prizegrades"][0]["typemoney"] != "" else "null"
            zusanNum = item["prizegrades"][1]["typenum"] if item["prizegrades"][1]["typenum"] != "" else "null"
            zusanMoney = item["prizegrades"][1]["typemoney"] if item["prizegrades"][1]["typemoney"] != "" else "null"
            zuliuNum = item["prizegrades"][2]["typenum"] if item["prizegrades"][2]["typenum"] != "" else "null"
            zuliuMoney = item["prizegrades"][2]["typemoney"] if item["prizegrades"][2]["typemoney"] != "" else "null"
            clearedData.append([phaseNo, date, week, winNumber[0], winNumber[1], winNumber[2], totalMoney, danxuanNum,
                                danxuanMoney, zusanNum, zusanMoney, zuliuNum, zuliuMoney])
        return clearedData
