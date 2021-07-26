from flask import Flask, request
from db.db_manager import DBManager
app = Flask(__name__)
db = DBManager()


@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    user = body['user']
    text = body['text']
    db.add(user, text)
    return body


@app.route('/msgs')
def all_messages():
    messages = db.read_all()
    return {'messages': messages}


@app.route('/whats_new', methods=['POST'])
def detect_new_messages():
    body = request.get_json()
    time = body['time']
    messages = db.read_new(time)
    return {'messages': messages}


@app.route('/is_online')
def is_online():
    return {'status': 'online'}


if __name__ == '__main__':
    app.run()

