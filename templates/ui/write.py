from pymongo import MongoClient
from flask import Flask, Blueprint, jsonify, request

write_blueprint = Blueprint('write', __name__)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree

# 글쓰기(POST) API
@write_blueprint.route('/writing', methods=['POST'])
def save_order():
    ids_receive = request.form['id']
    title_receive = request.form['title']
    url_receive = request.form['url']
    text_receive = request.form['text']

    doc = {
        'id' : ids_receive
        , 'title' : title_receive
        , 'url' : url_receive
        , 'text' : text_receive
    }

    db.writeGamePost.insert_one(doc)
    return jsonify({'msg': '작성이 완료되었습니다.'})
