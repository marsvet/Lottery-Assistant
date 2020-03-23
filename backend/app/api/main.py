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


# @api.route('/export_to_excel', methods=['POST'])
# def export2Excel():
#     filename = request.json['filename']
#     data = request.json['data']
#     filepath = './raw/%s.xlsx' % (filename)
#     excel.export2Excel(data, filepath)
#     return jsonify({
#         'success': True,
#         'url': filepath[1:]
#     })
