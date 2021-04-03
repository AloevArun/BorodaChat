from flask import Flask

version = '1.0'
app = Flask(__name__)


@app.route('/version')
def get_version():
    return 'BoroPDA ' + version


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
