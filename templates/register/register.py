from pymongo import MongoClient
import hashlib
from flask import Flask, Blueprint, jsonify, request

register_blueprint = Blueprint('register', __name__)

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree

# POST API

@register_blueprint.route('/setUser', methods=['POST'])
def setUser():
    # 회원정보 request
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    userName = request.form['userName_give']
    # 암호화
    password_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()

    exists = bool(db.account.find_one({"userID": userID}))
    if( exists == True):
        return jsonify({'result':'NO'})
    else:
        doc = {
            'userName': userName,
            'userPW': password_hash,
            'userID': userID
        }

        db.account.insert_one(doc)
        return  jsonify({'result':'YES'})

@register_blueprint.route('/idCheck', methods=['POST'])
def idCheck():
    #id 받아옴
    userID_receive = request.form['userID_give']
    #db에 있는 id와 체크
    exists = bool(db.account.find_one({"userID": userID_receive}))

    return jsonify({'result': 'success', 'exists': exists})

