from flask import Flask, request

from db.db_manager import DBManager

app = Flask(__name__)
db = DBManager()


@app.route('/msg', methods=['POST'])
def add_message():
    body = request.json
    user = body['user']
    text = body['text']
    db.add(user, text)
    return body


@app.route('/msgs')
def all_messages():
    messages = db.read_all()
    return {'messages': messages}

# @app.route('/is_ex')
# def detect_new_messages():
#     time = db.read_all()
#     return


# @app.route('/user/<string:name>/msg/<string:text>')
# def add_message_2(name, text):
#     print(f'Hello, {name} motherfucker!')
#     print(text)
#     return name


@app.route('/')
def hello_world():
    return {'name': 'Runya'}


@app.route('/online')
def online():
    pass


@app.route('/offline/<string:user>')
def offline(user):
    pass


@app.route('/status/<string:user>')
def status(user):
    return {'status': 'online'}


if __name__ == '__main__':
    app.run()
