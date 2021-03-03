from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, Blueprint, jsonify, request
from datetime import datetime, timedelta

login_blueprint = Blueprint('login', __name__)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree

@login_blueprint.route('/login', methods=['POST'])
def login():
    # 로그인
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    # 비밀번호 암호화
    pw_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()
    result = db.account.find_one({'userID': userID, 'userPW': pw_hash})

    if result is not None:
        payload = {
         'id': userID,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }

        # jwt token 생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        # decode = jwt.decode(token, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
