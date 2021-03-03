from pymongo import MongoClient
import hashlib
import datetime
from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import *

login_blueprint = Blueprint('login', __name__)

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree

def on_json_loading_failed_return_dict(e):
    return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@login_blueprint.route('/login', methods=['POST'])
def login():
    # 로그인

    login_data = request.get_json()
    userID = login_data['userID_give']
    userPW = login_data['userPW_give']
    pw_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()
    result = db.account.find_one({'userID' : userID, 'userPW' : pw_hash})
    current_Day = datetime.datetime.utcnow();
    expireTime = current_Day + datetime.timedelta(hours=1)

    if result is not None :
        return jsonify({'result': 'success', 'token': create_access_token(identity= userID, expires_delta= datetime.timedelta(hours=1))})
    else :
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
