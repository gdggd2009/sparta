from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

## Home
@app.route('/')
def home():
    return render_template('index.html')

## Save
@app.route('/memo', methods=['POST'])
def save():

    # 사용자에게서 입력받은 값
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # URL에 해당하는 HTML 가져오기
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    # 가져온 HTML을 파싱
    soup = BeautifulSoup(data.text, 'html.parser')

    # 파싱한 HTML에서 OG 태그 추출
    og_title = soup.select_one('meta[property="og:title"]')
    og_image = soup.select_one('meta[property="og:image"]')
    og_description = soup.select_one('meta[property="og:description"]')

    # 추출한 OG 태그의 컨텐츠 조회
    url_title = og_title['content']
    url_image = og_image['content']
    url_description = og_description['content']

    # DB에 저장하기 위한 데이터 생성
    article = {
        'url' : url_receive,
        'title' : url_title,
        'image' : url_image,
        'desc' : url_description,
        'comment' : comment_receive
    }

    # DB에 데이터 저장
    db.articles.insert_one(article)

    # 저장 성공 결과 반환
    return jsonify({'result':'success', 'msg':'등록 성공 했습니다.'})

## Find
@app.route('/memo', methods=['GET'])
def find():

    # DB에 저장된 값을 조회
    articles = list(db.articles.find({},{'_id':0}))

    # 조회한 값을 Client에 반환
    return jsonify({'result':'success', 'articles':articles})


if __name__ == '__main__' :
    app.run('0.0.0.0', port=5000, debug=True)
