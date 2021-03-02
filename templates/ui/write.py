from pymongo import MongoClient
from flask import Flask, Blueprint, jsonify, request
import re
import requests
from bs4 import BeautifulSoup

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
    naver_info = naver_main.find('div', class_='cm_info_box')
    naver_dt = naver_info.find_all('dt')
    naver_a = naver_info.find_all('a')
    naver_title = naver_main.find('div', class_='cm_top_wrap')


    #제목 크롤링
    title = naver_title.find('strong', class_='_text').text
    # print(title)

    #이미지 크롤링
    for img in naver_a:
        if img.find(text=re.compile("공식사이트")):
            break
    main = img['href']
    data = requests.get(main, headers=headers)
    gong = BeautifulSoup(data.text, 'html.parser')
    try:
        image = gong.select_one('meta[property="og:image"]')['content']
    except:
        image = gong.select_one('meta[name="og:image"]')['content']

    #한국어 지원 크롤링
    for korea in strong_things:
        if '한국어 지원' in korea.getText().lower():
            kor = korea.parent.parent.parent.text.partition('한국어 지원')[2].partition('[')[0]
            break
        else:
            kor = ''

    #게임등급
    for a_age in naver_dt:
        if a_age.find(text=re.compile("등급")):
            age = a_age.parent.text[5:]
            break
    # main_pack > section.sc_new.cs_common_module._cs_newgame.case_normal.color_3 > div.cm_top_wrap._sticky
    # sub_title

    #장르
    genre = naver_title.find('span', class_='txt').text

    #출시일
    for a_release in naver_dt:
        if a_release.find(text=re.compile("출시")):
            release = a_release.parent.text[4:]
            break

    #플랫폼
    for plat in naver_dt:
        if plat.find(text=re.compile("플랫폼")):
            platform = plat.parent.text[6:]
            break

    like = 0


    doc = {
        'id' : ids_receive,
        'game_name':title,
        'image':image,
        'kor':kor,
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
