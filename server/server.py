import os
from flask import Flask, request, url_for
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
    user_name = body['user_name']
    password = body['password']

    response = db.authentication(user_name, password)
    return response if response else {}


@app.route('/registration', methods=['POST'])
def registration():
    body = request.get_json()
    nickname = body['nickname']
    user_name = body['user_name']
    password = body['password']

    response = db.add_new_user(nickname, user_name, password)
    return response


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/msgs')
def all_messages():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    # messages = db.read_all_messages()
    # response = {'messages': messages}
    # return response


@app.route('/messages', methods=['POST'])
def get_user_messages():
    body = request.get_json()
    user = body['user']
    password = body['password']
    if db.authentication(user, password):
        messages = db.read_all_messages()
        user_messages = pack_data(user, messages)
        return user_messages
    else:
        user_messages = {"response": "denied"}
    return user_messages


@app.route('/whats_new', methods=['POST'])
def detect_new_messages(user):
    body = request.get_json()
    time = body['time']
    user = body['user']
    password = body['password']
    if db.authentication(user, password):
        messages = db.read_new_messages(time)
        user_messages = pack_data(user, messages)
        return user_messages
    else:
        return {"response": "denied"}


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
