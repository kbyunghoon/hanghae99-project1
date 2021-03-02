from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbgametree


# HTML 화면 호출
@app.route('/login')
def getLogin():
    return render_template('login.html')

@app.route('/register')
def getRegister():
    return render_template('register.html')

# POST API

@app.route('/setUser', methods=['POST'])
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

    db.gametree.insert_one(doc)

    return jsonify({'msg': '회원가입이 완료되었습니다.'})

#GET APT
@app.route('/idCheck', methods=['POST'])
def idCheck():

    userID_receive = request.form['userID_give']
    exists = bool(db.gametree.find_one({"userID": userID_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/login', methods=['POST'])
def login():
    # 로그인
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    pw_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()
    result = db.gametree.find_one({'userID': userID, 'userPW': pw_hash})

    if result is not None:
        payload = {
         'id': userID,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000, debug=True)



