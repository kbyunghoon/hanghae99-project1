from pymongo import MongoClient
from flask import Flask, Blueprint, jsonify, request
import re
import requests
from bs4 import BeautifulSoup
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
def save_gameinfo():
    ids_receive = request.form['id']
    title_receive = request.form['title']
    text_receive = request.form['text']
    search = request.form['url']
    namu = 'https://namu.wiki/w/' + search
    naver = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query=' + search
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(namu, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    strong_things = soup.find_all('strong')
    # a_things = soup.find_all('a')
    # span_things = soup.find_all('span')
    data_naver = requests.get(naver, headers=headers)
    naver_main = BeautifulSoup(data_naver.text, 'html.parser')
    gameYn = naver_main.select('.cs_common_module > div > div > div > span')[0]
    if gameYn.find('게임') == -1:
        return jsonify({'msg': '해당 키워드를 다시 확인해주세요.'})
    naver_info = naver_main.find('div', class_='cm_info_box')
    naver_dt = naver_info.find_all('dt')
    naver_a = naver_info.find_all('a')
    naver_title = naver_main.find('div', class_='cm_top_wrap')

    #제목 크롤링
    title = naver_title.find('strong', class_='_text').text

    #이미지 + 공식홈페이지 크롤링
    for img in naver_a:
        if img.find(text=re.compile("공식사이트")):
            break
    main = img['href']
    data = requests.get(main, headers=headers, verify=False)
    gong = BeautifulSoup(data.text, 'html.parser')
    image = naver_main.find('div', class_='detail_info').select('a > img')[0]['src']
    # print(image)

    for lounge in naver_a: #언어, 가격, 장르, 등급, 출시일, 플랫폼 크롤링
        if lounge.find(text=re.compile("게임라운지 더보기")):
            thelink = lounge['href'].replace("https://game.naver.com/r/","").replace("/home","")
            break
    api = 'https://apis.naver.com/nng_main/nng_main/game/info/' + thelink
    api_info = requests.get(api, headers=headers)
    json_data = json.loads(api_info.text)
    game_info = json_data['result']['contentInfo']
    lang = game_info['language']
    price = game_info['price']
    genre = game_info['genre']
    a_age = game_info['contentsRating'].split(',')
    age = []
    for age_split in a_age:
        age.append(age_split.strip())
    release = game_info['releaseDate']
    platform = game_info['platformInfo']['platform'].replace(" ",'').split(',')
    like = 0


    doc = {
        'id' : ids_receive,
        'game_name':title,
        'image':image,
        'price':price,
        'lang':lang,
        'genre':genre,
        'age':age,
        'release':release,
        'platform':platform,
        'homepage':main,
        'text' : text_receive,
        'like' : like
    }

    db.writeGamePost.insert_one(doc)
    return jsonify({'msg': '작성이 완료되었습니다.'})
