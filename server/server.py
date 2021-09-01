import os
from flask import Flask, request, jsonify
from db.db_manager import User, Message

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.curdir), "instance"))
msg = Message()
usr = User()
print(usr.get_all())


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    login = body['login']
    password = body['password']

    response = usr.login(login, password)
    return response if response else {}


@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    login = body['login']
    password = body['password']
    response = usr.create(nickname, login, password)
    return response


@app.route('/users', methods=['POST'])
def get_users():
    body = request.get_json()
    login = body['login']
    password = body['password']
    if usr.login(login, password) != 'denied':
        response = usr.get_all()
    else:
        response = {'response': 'non_authorized'}
    return jsonify(response)


@app.route('/messages', methods=['POST'])
def get_messages():
    body = request.get_json()
    user = body['login']
    password = body['password']
    nickname = usr.login(user, password)['response']
    time = body['time']

    if nickname != 'denied':
        messages = {"messages": msg.read(time)}
        if len(messages['messages']) != 0:
            try:
                response = sort_messages(nickname, messages)
            except all:
                response = {"response": 'dict_error'}
        else:
            response = {"response": "no_messages"}
    else:
        response = {"response": "non_authorized"}
    print(response)
    return response


@app.route('/add_message', methods=['POST'])
def add_message():
    body = request.get_json()
    sender = usr.login(body['login'], body['password'])['response']
    if sender != 'denied':
        receiver = body['receiver']
        text = body['text']
        msg.add(sender, receiver, text)
        return 'done'
    else:
        return 'unauthorized'


@app.route('/is_online')
def is_online():
    response = {'status': 'online'}
    return response


def sort_messages(user: str, messages: dict):
    user_messages = {}
    for message in messages['messages']:
        users = message['sender'], message['receiver']

        if 'global_chat' != message['receiver']:
            if user not in users:
                continue

        if user == message['sender'] or 'chat' in message['receiver']:
            key = 'receiver'
        else:
            key = 'sender'

        if not user_messages.get(message[key]):
            user_messages[message[key]] = []

        user_messages[message[key]].append(message)
    return user_messages if user_messages else {"response": 'no_user_messages'}


if __name__ == '__main__':
    app.run()
