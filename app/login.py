from flask import render_template, request, session, redirect, url_for
from app import app
from app import user
import config
import sqlite3
from sqlite3 import Error
import psycopg2
import os


def get_db():
    if config.testing:
        db = psycopg2.connect(config.database_path)

    else:
        db = psycopg2.connect(os.environ['DATABASE_URL'])

    return db


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        # for creation of the Account
        if "success" in session:
            success = session['success']
            session.pop('success', None)
            return render_template('login.html', created=success)
        # for people trying to trick them into remaking the session
        if "username" in session:
            return "You are logged in as %s, please logout before trying to login again." % session["username"]
        # normal get method login
        else:
            return render_template('login.html')
    if request.method == 'POST':
        data = request.form
        start_session(data)
        if 'username' in session:
            # Logs in & Directs to HomePage
            return redirect(url_for("hello_world"))
        else:
            return render_template('login.html', success=False)


def start_session(data):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE email = '%s' AND password = '%s';""" % (data['email'].lower(), data['password']))
    user_data = c.fetchone()
    if user_data is None:
        return "Email or Password was Entered incorrectly"
    else:
        grabbed_user = user.User(user_data[1], user_data[2], user_data[3], user_data[4], user_data[0], user_data[5])
        try:
            c.execute('''UPDATE users SET last_time_stamp = '%s' WHERE username = '%s';''' % (grabbed_user.last_visit, grabbed_user.username))
            conn.commit()
        except Error:
            print "Could not update last visit timestamp"
        set_session(grabbed_user)


def set_last_visit(last_visit):
    if last_visit is None:
        time = datetime.datetime.now().strftime("%m/%d/%y - %H:%M")
    return time


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
