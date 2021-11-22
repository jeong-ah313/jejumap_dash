from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('mongodb://test:test@54.180.143.57', 27017)
#client = MongoClient('localhost', 27017)
db = client.mapJEJU

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/travel')
def travel():
    return render_template('travel.html')

@app.route('/hotel')
def hotel():
    return render_template('hotel.html')

@app.route('/food')
def food():
    return render_template('food.html')

#DB불러오기
@app.route('/getfood', methods=['GET'])
def Food():
    data_food = list(db.FOOD.find({ }, {'_id': False}))
    return jsonify({'msg': 'success', 'data': data_food})

@app.route('/gethotel', methods=['GET'])
def Hotel():
    data_hotel = list(db.HOTEL.find({ }, {'_id': False}))
    return jsonify({'msg': 'success', 'data': data_hotel})

@app.route('/gettravel', methods=['GET'])
def Travel():
    data_travel = list(db.TRAVEL.find({ }, {'_id': False}))
    return jsonify({'msg': 'success', 'data': data_travel})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


