from flask import render_template, request, session, redirect, url_for
from app import app
from app import user
import config
import sqlite3


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if "username" in session:
            return "You are logged in as %s, please logout before trying to login again." % session["username"]
        else:
            return render_template('login.html')
    if request.method == 'POST':
        data = request.form
        print start_session(data)
        if 'username' in session:
            # Logs in & Directs to HomePage
            return redirect(url_for("hello_world"))
        else:
            return render_template('login.html', success=False)


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


def set_session(user_name):
    session['id'] = user_name.identifier
    session['username'] = user_name.username
    session['status'] = user_name.status


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('status', None)
    # TODO Create Logout Page (If not happy with below method)
    return redirect(url_for("hello_world"))
