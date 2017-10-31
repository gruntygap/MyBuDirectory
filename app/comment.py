from flask import render_template
from app import app
import config
import datetime
import uuid
import sqlite3
from sqlite3 import Error


@app.route('/comments')
def comments():
    # TODO Load comments once feature is added
    return render_template('comments.html')


@app.route('/comments/new')
def new_comment():
    create_comment("dick", "dicks")

    return render_template('newCommentForm.html')


def create_comment(author, content):
    comment = Comment(author, content)
    print comment.identifier
    upload_comment(comment)


def upload_comment(comment):
    # Adds new
    conn = sqlite3.connect(config.database_path)
    c = conn.cursor()

    # Create table
    try:
        c.execute('''CREATE TABLE comments
                         (id TEXT, author TEXT, content TEXT, time_stamp TEXT)''')
    except Error:
        # Do nothing in particular
        print "Will not re-create"

    data = [(comment.identifier, comment.author, comment.content, comment.time_stamp)]
    # Insert a row of data
    c.executemany("INSERT INTO comments VALUES (?,?,?,?)", data)
    # Saves
    conn.commit()

@app.route('/comments/delete/<identifier>')
def delete_comment(identifier):
    conn = sqlite3.connect(config.database_path)
    try:
        conn.cursor().execute("DELETE FROM comments WHERE id=?", (identifier,))
        conn.commit()
        return "Deleted: %s" % identifier
    except Error as e:
        return "Could not delete %s" % e


# Comment Object
class Comment:

    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.time_stamp = self.set_time_stamp()
        self.identifier = self.set_identifier()

    def get_content(self):
        return self.content

    def get_author(self):
        return self.author

    @staticmethod
    def set_time_stamp():
        # creates time stamp of creation of the comment
        time = datetime.datetime.now().isoformat()
        return time

    @staticmethod
    def set_identifier():
        # Generates identifier - takes the first 8 characters
        # TODO May create collisions, when that happens, will have to replace method
        # http://hashids.org/python/
        identifier = str(uuid.uuid4())[:8]
        return identifier
