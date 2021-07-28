from flask import Flask, request

from db.db_manager import DBManager

app = Flask(__name__)
db = DBManager()


@app.route('/msg', methods=['POST'])
def add_message():
    body = request.get_json()
    sender = body['sender']
    receiver = body['receiver']
    text = body['text']
    db.add_new_message(sender, receiver, text)
    return '201'


# @app.route('/new_dialog', methods=['POST'])
# def new_dialog():
#     body = request.get_json()
#     creator = body['creator']
#     guest = body['guest']
#     response = db.create_new_dialog_table(creator, guest)
#     return response


@app.route('/user', methods=['POST'])
def login():
    body = request.get_json()
    user = body['user']
    password = body['password']
    response = db.authentification(user, password)
    return response


@app.route('/registration', methods=['POST'])
def register():
    body = request.get_json()
    user = body['user']
    password = body['password']
    response = db.add_new_user(user, password)
    return response


@app.route('/msgs')
def all_messages():
    messages = db.read_all_messages()
    response = {'messages': messages}
    return response


@app.route('/messages/<string:user>')
def get_user_messages(user):
    messages = db.read_all_messages()
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


@app.route('/whats_new', methods=['POST'])
def detect_new_messages():
    body = request.get_json()
    time = body['time']
    messages = db.read_new_messages(time)
    response = {'messages': messages}
    return response


@app.route('/is_online')
def is_online():
    response = {'status': 'online'}
    return response


if __name__ == '__main__':
    app.run()

# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     body = request.get_json()
#     user = body['user']
#     db.delete_user(user)
#     return body
