from . import blue
from flask import jsonify, request
from app import mongo

res = {'code': 200, 'msg': '成功', 'success': True}

error = {'code': 100, 'msg': '出错了', 'success': False}


@blue.route('/test', methods=['GET'])
def test():
    print(request.method)
    return jsonify(res)
