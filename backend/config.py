# -*-coding:utf-8-*-
#
# 配置文件
#
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hard to guess string."
    JSON_AS_ASCII = False
    JOBS = [
        {
            'id': 'updateDB',
            'func': 'app.tasks:updateDB',
            'trigger': 'cron',
            'hour': '8',
            # 'minute': '30'
        }
    ]
