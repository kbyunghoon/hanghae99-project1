from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

mypage_blueprint = Blueprint('mypage', __name__)

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbGameTree


# POST API

@mypage_blueprint.route('/getMypage', methods=['POST'])
def getMypage():
    userID = request.form['userID_give']
    user_info = db.account.find_one({"userID": userID}, {"_id": False})

    return jsonify({'user':user_info})




@mypage_blueprint.route('/userUpdate', methods=['POST'])
def userUpdate():
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    password_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()
    print(userID)
    print(userPW)
    result = bool(db.account.update_one({'userID':userID},{'$set':{'userPW':password_hash}}))

    if(result == True):
        return jsonify({'msg':'succes'})