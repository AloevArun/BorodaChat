import os
from flask import Flask, request
from db.db_manager import DBManager

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.curdir), "instance"))
db = DBManager()


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
    sender = db.login(body['login'], body['password'])['response']
    if sender != 'denied':
        receiver = body['receiver']
        text = body['text']
        db.add_new_message(sender, receiver, text)
        return 'done'
    else:
        return 'non_authorized'


# проверка пароля(+++)
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    nickname = body['login']
    password = body['password']

    response = db.login(nickname, password)
    return response if response else {}


# создание новой записи для нового пользователя(+++)
@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    user_name = body['login']
    password = body['password']

    response = db.add_new_user(nickname, user_name, password)
    return response


# получить все сообщения и запаковать(+++)
@app.route('/messages', methods=['POST'])
def get_user_messages():
    body = request.get_json()

    user = body['login']
    password = body['password']
    nickname = db.login(user, password)['response']
    method = body['method']
    time = body['time'] if method == 'update' else '0001-01-01T0:00:00.00'

    if nickname != 'denied':
        if method == 'all':
            messages = {"messages": db.read_all_messages()}
        else:
            messages = {"messages": db.read_all_messages(is_update=True, time=time)}
        if len(messages['messages']) != 0:
            try:
                response = sort_messages(nickname, messages)
            except all:
                response = {"response": 'db_error'}
        else:
            response = {"response": "no_messages"}
    else:
        response = {"response": "non_authorized"}
    return response


# простой пинг(+++)
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


#  # получить все сообщения отправленные после time и запаковать(---)
#  @app.route('/whats_new', methods=['POST'])
#  def detect_new_messages():
#      body = request.get_json()
#      user = body['login']
#      password = body['password']
#      nickname = db.login(user, password)['response']
#      time = body['time']
#      if nickname != 'denied':
#          messages = {"messages": db.read_new_messages(time)}
#          print(len(messages), messages)
#          if len(messages['messages']) != 0:
#              try:
#                  response = pack_data(nickname, messages)
#              except all:
#                  response = {"response": 'db_error'}
#          else:
#              response = {"response": "no_messages"}
#      else:
#          response = {"response": "non_authorized"}
#      return response
