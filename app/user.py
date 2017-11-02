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
    create_user(data['username'], data['email'], data['pass'])
    return "Good"


def check_user():
    # Checks if username is available
    pass


def create_user(username, email, password):
    new_person = User(username, email, password)
    print new_person.username
    print new_person.email
    print new_person.password
    print new_person.identifier
    print new_person.day_created
    print new_person.last_visit
    pass


def upload_user():
    pass


def delete_user():
    pass


def activate_user():
    pass


class User:

    def __init__(self, username, email, password, identifier=None, day_created=None, last_visit=None):
        self.username = username
        self.email = email
        self.password = password
        self.day_created = self.set_time_stamp(day_created)
        self.last_visit = self.set_last_visit(last_visit)
        self.identifier = self.set_identifier(identifier)

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
