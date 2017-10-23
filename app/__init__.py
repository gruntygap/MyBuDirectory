from flask import Flask, render_template


app = Flask(__name__)
from app import cookie
from direct import direct
from app import comment
from app import help
from app import login


@app.route('/')
def hello_world():
    return render_template('index.html')
