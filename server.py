from flask import Flask
from playsound import playsound
version = '1.0'
app = Flask(__name__)


@app.route('/msg')
def get_message():
    return 'BoroPDA ' + version


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

