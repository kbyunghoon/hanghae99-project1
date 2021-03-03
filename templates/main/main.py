from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

main_blueprint = Blueprint('main', __name__)

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbGameTree


@main_blueprint.route('/write', methods=['GET'])
def listing():
    games = list(db.writeGamePost.find({}, {'_id': False}).sort("like", -1))
    return jsonify({'all_game_data':games})

@main_blueprint.route('/like', methods=['POST'])
def like_game():
    title_receive = request.form['title']
    targeting = db.writeGamePost.find_one({'game_name': title_receive})
    current_like = targeting['like']
    new_like = current_like + 1
    db.writeGamePost.update_one({'game_name': title_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': title_receive + '를 추천하셨습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)