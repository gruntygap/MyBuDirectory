from flask import render_template, request, session, redirect, url_for
from app import app
from app import comment
import config
import datetime
import uuid
import sqlite3
from exceptions import ValueError
from sqlite3 import Error


@app.route('/user/new', methods=['POST'])
def new_user():
    # TODO fix the order of which tables are created.
    data = request.form
    try:
        # Tests the UserName
        success = check_user(data['newUsername']), " created User"
        # If the program makes it here, the username is unique: Continue making a user
        create_user(data['newUsername'], data['newEmail'], data['newPassword'])
    except ValueError:
        success = "The username already exists, did not create User"
        # TODO return duplicate user error to the HTMl
    # return success
    session['success'] = success
    return redirect(url_for('login'))


# Checks if username is available
def check_user(username):
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()
    c.execute('''SELECT username FROM users WHERE username = "%s";''' % username)
    if c.fetchone() is None:
        return "Username is Available!"
    else:
        raise ValueError()


def create_user(username, email, password):
    new_person = User(username, email, password)
    upload_user(new_person)


# Handles Creation of the SQL as well as insertion
def upload_user(user):
    # Adds new
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()

    # Create table
    try:
        c.execute('''CREATE TABLE users
                             (id TEXT, username TEXT, email TEXT, password TEXT, status TEXT, creation_time_stamp TEXT, last_time_stamp TEXT)''')
    except Error:
        # Do nothing in particular
        print "Table Already Exists"

    data = [(user.identifier, user.username, user.email.lower(), user.password, user.status, user.day_created,
             user.last_visit)]
    # Insert a row of data
    c.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", data)
    # Saves
    conn.commit()


@app.route('/user/delete')
def delete_user(identifier):
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM users WHERE id='%s';''' % identifier)
    except Error:
        print "Could not delete"
    conn.commit()


@app.route('/user/admin/<username>/<password>')
def admin_user(username, password):
    if password == config.secret:
        conn = sqlite3.connect(config.database_path)
        c = conn.cursor()
        # Create table
        try:
            c.execute('''UPDATE users SET status = 'admin' WHERE username = "%s";''' % username)
        except Error:
            print "Could not update"
        conn.commit()
        return "Greaaatttt!"
    else:
        return "Not correct Password"


@app.route('/password/reset')
def forgot_pass():
    return "Well I guess you're screwed? Contact Admin with Help?"


@app.route('/user/profile')
def user_profile():
    if "username" in session:
        return render_template('profile.html')
    else:
        return "This is all just a dream, return from whence you came."


@app.route('/user/admin')
def admin_menu():
    if 'status' in session:
        if session['status'] == "admin":
            users = get_users()
            comments = comment.get_comments()
            return render_template('admin.html', users=users, comments=comments)
    else:
        return "This is all just a dream, return from whence you came."


def get_users():
    users = []
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    results = c.fetchall()
    for result in results:
        users.append(User(result[1], result[2], result[3], result[4], result[0], result[6], result[5]))
    return users


class User:
    def __init__(self, username, email, password, status=None, identifier=None, day_created=None, last_visit=None):
        self.username = username
        self.email = email
        self.password = password
        self.status = self.set_status(status)
        self.day_created = self.set_time_stamp(day_created)
        self.last_visit = self.set_last_visit(last_visit)
        self.identifier = self.set_identifier(identifier)

    @staticmethod
    def set_status(status):
        if status is None:
            status = "user"
        return status

    @staticmethod
    def set_time_stamp(time_stamp):
        if time_stamp is None:
            # creates time stamp of creation of the comment
            time = datetime.datetime.now().strftime("%m/%d/%y - %H:%M")

            return time
        else:
            return time_stamp

    @staticmethod
    def set_last_visit(last_visit):
        if last_visit is None:
            last_visit = datetime.datetime.now().strftime("%m/%d/%y - %H:%M")
        return last_visit

    @staticmethod
    def set_identifier(identifier):
        if identifier is None:
            # Generates identifier - takes the first 8 characters
            # TODO May create collisions, when that happens, will have to replace method
            # http://hashids.org/python/
            identifier = str(uuid.uuid4())[:8]
            return identifier
        else:
            return identifier
