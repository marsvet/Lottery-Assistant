# -*-coding:utf-8-*-
from flask import request, jsonify
from app.api import api
from app import db
# import app.excel as excel


@api.route('/winning_data')
def getWinningData():
    winning_data = db.getWinningData()
    result = {
        'success': True,
        'data': [list(item) for item in winning_data]
    }
    return jsonify(result)
