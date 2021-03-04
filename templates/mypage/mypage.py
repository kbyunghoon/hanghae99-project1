from pymongo import MongoClient
import hashlib
from flask import Flask, jsonify, request, Blueprint
mypage_blueprint = Blueprint('mypage', __name__)

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbGameTree


# POST API

@mypage_blueprint.route('/userUpdate', methods=['POST'])
def userUpdate():
    userID = request.form['userID_give']
    userPW = request.form['userPW_give']
    password_hash = hashlib.sha256(userPW.encode('utf-8')).hexdigest()
    result = bool(db.account.update_one({'userID':userID},{'$set':{'userPW':password_hash}}))

    if(result == True):
        return jsonify({'msg':'succes'})