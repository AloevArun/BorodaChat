import os
from flask import Flask, request
from db.db_manager import DBManager

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.curdir), "instance"))
db = DBManager()


# проверка пароля(+++)
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    nickname = body['login']
    password = body['password']

    response = db.User.login(nickname, password)
    return response if response else {}


# создание новой записи для нового пользователя(+++)
@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    user_name = body['login']
    password = body['password']
    response = db.User.create(nickname, user_name, password)
    return response


# получить все сообщения и запаковать(+++)
@app.route('/messages', methods=['POST'])
def get_messages():
    body = request.get_json()

    user = body['login']
    password = body['password']
    nickname = db.User.login(user, password)['response']
    method = body['method']
    time = body['time'] if method == 'update' else '0001-01-01T0:00:00.00'

    if nickname != 'denied':
        messages = {"messages": db.Message.read(time)}
        if len(messages['messages']) != 0:
            try:
                response = sort_messages(nickname, messages)
            except all:
                response = {"response": 'dict_error'}
        else:
            response = {"response": "no_messages"}
    else:
        response = {"response": "non_authorized"}
    return response


# раскидать сообщения по адресатам в словарь(+++)
def sort_messages(user: str, messages: dict):
    user_messages = {}
    for message in messages['messages']:
        users = message['sender'], message['receiver']

        if 'chat' != message['receiver']:
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


# добавление сообщения в базу(+++)
@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    sender = db.User.login(body['login'], body['password'])['response']
    if sender != 'denied':
        receiver = body['receiver']
        text = body['text']
        db.Message.add(sender, receiver, text)
        return 'done'
    else:
        return 'non_authorized'


# простой пинг(+++)
@app.route('/is_online')
def is_online():
    response = {'status': 'online'}
    return response


if __name__ == '__main__':
    app.run()
