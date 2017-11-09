from flask import render_template, request
from app import app
from app import user
import config
import sqlite3

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = request.form
        print data['email']
        print data['password']
        print start_session(data)
        return render_template('index.html')


def start_session(data):
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()
    c.execute('''SELECT * FROM users
                  WHERE users.email = "%s"
                  AND users.password = "%s"''' % (data['email'].lower(), data['password']))
    user_data = c.fetchone()
    if user_data is None:
        return "Email or Password was Entered incorrectly"
    else:
        grabbed_user = user.User(user_data[1], user_data[2], user_data[3], user_data[4], user_data[0], user_data[5])
        set_session(grabbed_user)
        return "Email or Password was Entered right boi"


def set_session(user):
    pass


def logout():
    pass