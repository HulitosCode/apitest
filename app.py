from flask import Flask

app = Flask(__name__)

from controller import *


@app.route("/")
def index():
    return "Ola Mundo"
        


