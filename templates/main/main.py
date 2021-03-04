from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

main_blueprint = Blueprint('main', __name__)

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbGameTree

@main_blueprint.route('/like', methods=['POST'])
def like_game():
    title_receive = request.form['title']
    targeting = db.writeGamePost.find_one({'game_name': title_receive})
    current_like = targeting['like']
    new_like = current_like + 1
    db.writeGamePost.update_one({'game_name': title_receive}, {'$set': {'like': new_like}})
    return jsonify({})