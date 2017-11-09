from flask import render_template, request
from app import app
import config
import datetime
import uuid
import sqlite3
from sqlite3 import Error


@app.route('/user/new', methods=['POST'])
def new_user():
    data = request.form
    try:
        # Tests the UserName
        success = check_user(data['username'])
        # If the program makes it here, the username is unique: Continue making a user
        create_user(data['username'], data['email'], data['pass'])
    except ValueError, e:
        print e
        success = e
        # TODO return duplicate user error to the HTMl
    return success


# Checks if username is available
def check_user(username):
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()
    c.execute('''SELECT username FROM users WHERE username = "%s";''' % username)
    if c.fetchone() is None:
        return "Username is Available!"
    else:
        raise ValueError("The username already exists")


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

    data = [(user.identifier, user.username, user.email.lower(), user.password, user.status, user.day_created, user.last_visit)]
    # Insert a row of data
    c.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", data)
    # Saves
    conn.commit()


def delete_user():
    pass


def activate_user():
    pass


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
            time = datetime.datetime.now().strftime("%m/%d/%y - %H:%M")
        return time

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
