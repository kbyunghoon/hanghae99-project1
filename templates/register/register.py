from pymongo import MongoClient
import hashlib
from flask import Flask, Blueprint, jsonify, request

register_blueprint = Blueprint('register', __name__)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree

# POST API

@register_blueprint.route('/setUser', methods=['POST'])
def setUser():
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    userName = request.form['userName_give']
    password_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()

    doc = {
        'userName':userName,
        'userPW': password_hash,
        'userID':userID
    }

    db.account.insert_one(doc)

    return jsonify({'msg': '회원가입이 완료되었습니다.'})

#GET APT
@register_blueprint.route('/idCheck', methods=['POST'])
def idCheck():

    userID_receive = request.form['userID_give']
    exists = bool(db.account.find_one({"userID": userID_receive}))
    return jsonify({'result': 'success', 'exists': exists})

