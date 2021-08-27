import os
from flask import Flask, request
from db.db_manager import DBManager

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.curdir), "instance"))
db = DBManager()


# раскидать сообщения по адресатам в словарь
def pack_data(user: str, messages: dict):
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
    return user_messages if user_messages else 'no_messages'


# добавление сообщения в базу
@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    sender = db.login(body['login'], body['password'])['response']
    if sender != 'denied':
        receiver = body['receiver']
        text = body['text']
        db.add_new_message(sender, receiver, text)
        return 'done'
    else:
        return 'non_authorized'


# проверка пароля
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    nickname = body['login']
    password = body['password']

    response = db.login(nickname, password)
    return response if response else {}


# создание новой записи для нового пользователя
@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    user_name = body['login']
    password = body['password']

    response = db.add_new_user(nickname, user_name, password)
    return response


# получить все сообщения(не актуально)
@app.route('/msgs')
def all_messages():
    messages = db.read_all_messages()
    response = {'messages': messages}
    return response


# получить все сообщения и запаковать
@app.route('/messages', methods=['POST'])
def get_user_messages():
    body = request.get_json()
    user = body['login']
    password = body['password']
    nickname = db.login(user, password)['response']
    if nickname != 'denied':
        messages = {"messages": db.read_all_messages()}
        print(len(messages), messages)
        if len(messages['messages']) != 0:
            try:
                response = pack_data(nickname, messages)
            except TypeError:
                response = {"response": 'no_messages_for_user'}
        else:
            response = {"response": "no_messages"}
    else:
        response = {"response": "non_authorized"}
    return response


# получить все сообщения отправленные после time и запаковать
@app.route('/whats_new', methods=['POST'])
def detect_new_messages():
    body = request.get_json()
    time = body['time']
    user = body['user']
    password = body['password']
    if db.login(user, password):
        messages = db.read_new_messages(time)
        if len(messages) != 0:
            user_messages = pack_data(user, messages)
            return user_messages
        else:
            return {"response": "no_updates"}
    else:
        return {"response": "non_authorized"}


# простой пинг
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
