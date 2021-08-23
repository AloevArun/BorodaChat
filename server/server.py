import os
from flask import Flask, request
from db.db_manager import DBManager

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.curdir), "instance"))
db = DBManager()


def pack_data(user: str, messages: dict):
    user_messages = {}
    for message in messages:
        users = message['sender'], message['receiver']

        if 'chat' != message['receiver']:
            if user not in users:
                continue

        key = 'receiver' if user == message['sender'] or 'chat' in message['receiver'] else 'sender'
        if not user_messages.get(message[key]):
            user_messages[message[key]] = []

        user_messages[message[key]].append(message)
        return user_messages


@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    sender = body['sender']
    receiver = body['receiver']
    text = body['text']
    db.add_new_message(sender, receiver, text)
    return '201'


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    nickname = body['login']
    password = body['password']

    response = db.authentication(nickname, password)
    return response if response else {}


@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    user_name = body['login']
    password = body['password']

    response = db.add_new_user(nickname, user_name, password)
    return response


@app.route('/msgs')
def all_messages():
    messages = db.read_all_messages()
    response = {'messages': messages}
    return response


@app.route('/messages', methods=['POST'])
def get_user_messages():
    body = request.get_json()
    user = body['user']
    password = body['password']

    if db.authentication(user, password):
        messages = db.read_all_messages()
        if len(messages) != 0:
            user_messages = pack_data(user, messages)
            return user_messages
        else:
            return {"response": "no_updates"}
    else:
        return {"response": "non_authorized"}


@app.route('/whats_new', methods=['POST'])
def detect_new_messages():
    body = request.get_json()
    time = body['time']
    user = body['user']
    password = body['password']
    if db.authentication(user, password):
        messages = db.read_new_messages(time)
        if len(messages) != 0:
            user_messages = pack_data(user, messages)
            return user_messages
        else:
            return {"response": "no_updates"}
    else:
        return {"response": "non_authorized"}


@app.route('/is_online')
def is_online():
    response = {'status': 'online'}
    return response


if __name__ == '__main__':
    app.run()

# @app.route('/new_dialog', methods=['POST'])
# def new_dialog():
#     body = request.get_json()
#     creator = body['creator']
#     guest = body['guest']
#     response = db.create_new_dialog_table(creator, guest)
#     return response
