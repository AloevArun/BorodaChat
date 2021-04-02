from flask import Flask
from playsound import playsound

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


playsound('pda.mp3')

if __name__ == '__main__':
    app.run()
