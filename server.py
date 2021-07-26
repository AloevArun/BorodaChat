from flask import Flask, request

from db.db_manager import DBManager

app = Flask(__name__)
db = DBManager()


@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    user = body['user']
    text = body['text']
    db.add_new_message(user, text)
    return body


@app.route('/user', methods=['POST'])
def login():
    body = request.get_json()
    user = body['user']
    password = body['password']
    answer = db.authentification(user, password)
    return answer


@app.route('/registration', methods=['POST'])
def register():
    body = request.get_json()
    user = body['user']
    password = body['password']
    status = db.add_new_user(user, password)
    if not status:
        return 'User already exists!'
    else:
        return 'Done!'


@app.route('/msgs')
def all_messages():
    messages = db.read_all_messages()
    return {'messages': messages}


@app.route('/whats_new', methods=['POST'])
def detect_new_messages():
    body = request.get_json()
    time = body['time']
    messages = db.read_new_messages(time)
    return {'messages': messages}


@app.route('/is_online')
def is_online():
    return {'status': 'online'}


if __name__ == '__main__':
    app.run()

# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     body = request.get_json()
#     user = body['user']
#     db.delete_user(user)
#     return body
