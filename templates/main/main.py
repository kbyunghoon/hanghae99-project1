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

## API 역할을 하는 부분
@main_blueprint.route('/write', methods=['POST'])
def saving():
    search = request.form['name_give']
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
    print(title)

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

    #게임등급
    for a_age in naver_dt:
        if a_age.find(text=re.compile("등급")):
            age = a_age.parent.text[5:]
            break

    #장르
    for a_gen in strong_things:
        if '장르' in a_gen.getText().lower():
            genre = a_gen.parent.parent.parent.text[2:]
            break

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


    doc = {
        'title':title,
        'image':image,
        'kor':kor,
        'genre':genre,
        'age':age,
        'release':release,
        'platform':platform,
        'homepage':gong,
        'nickname':nickname
    }
    db.writeGamePost.insert_one(doc)
    return jsonify({'msg':'저장 완료'})
    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)