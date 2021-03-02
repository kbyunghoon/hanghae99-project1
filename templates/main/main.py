import re
import requests
from flask import Flask, Blueprint, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient

main_blueprint = Blueprint('main', __name__)

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbGameTree


@main_blueprint.route('/write', methods=['GET'])
def listing():
    games = list(db.writeGamePost.find({}, {'_id': False}))
    return jsonify({'all_game_data':games})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)