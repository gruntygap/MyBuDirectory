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
    print data['username']
    print data['email']
    print data['pass']
    return "Good"


def check_user():
    # Checks if username is available
    pass


def create_user():
    pass


def upload_user():
    pass


def delete_user():
    pass


def activate_user():
    pass


class User:

    def __init__(self, username, email, password, day_created, last_visit, activated, identifier):
        self.username = username
        self.email = email
        self.password = password
        self.day_created = day_created
        self.last_visit = last_visit
        self.activated = activated
        self.identifier = identifier
