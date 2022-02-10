from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def get_info():
    variavel = os.environ.get('TOKEN_TELEGRAM')
    return variavel

if __name__ == '__main__':
    app.run(debug=True)