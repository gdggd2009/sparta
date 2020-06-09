from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def listing():
    orders = list(db.orders.find({},{'_id':0}))
    return jsonify({'result':'success', 'orders': orders})

@app.route('/list', methods=['POST'])
def saving():
    name_receive = request.form['name_give']
    size_receive = request.form['size_give']
    use_receive = request.form['use_give']
    please_receive = request.form['please_give']

    order = {
        'name': name_receive,
        'size': size_receive,
        'use': use_receive,
        'please':please_receive
    }

    db.orders.insert_one(order)

    return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)
