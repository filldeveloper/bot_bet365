from flask import Flask
from functions import mensagem_bot_telegram

app = Flask(__name__)

@app.route('/')
def get_info():
    return 'Hello, Caramba!'

if __name__ == '__main__':
    app.run(debug=True)