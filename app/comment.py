from flask import render_template, request
from app import app
import config
import datetime
import uuid
from sqlite3 import Error
import psycopg2
import os
# for emoji support
import sys
reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/comments')
def start_comments():
    comments = get_comments()
    # Reverses the Array to make it chronologically accurate
    comments = reversed(comments)
    return render_template('comments.html', comments=comments)


def get_db():
    if config.testing:
        db = psycopg2.connect(config.database_path)

    else:
        db = psycopg2.connect(os.environ['DATABASE_URL'])

    return db


@app.route('/comments/new', methods=['POST'])
def new_comment():
    data = request.form
    create_comment(data['name'], data['message'])
    return "Post Created!"


def create_comment(author, content):
    comment = Comment(author, content)
    upload_comment(comment)


def upload_comment(comment):
    # Adds new
    conn = get_db()
    cur = conn.cursor()

    # TODO Add support for ' and "
    # Insert a row of data
    sql = "INSERT INTO comments VALUES ('%s','%s','%s','%s')" % (comment.identifier, comment.author, comment.content, comment.time_stamp)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


@app.route('/comments/delete/<identifier>')
def delete_comment(identifier):
    conn = get_db()
    cur = conn.cursor()
    if identifier == "all":
        cur.execute("DELETE FROM comments;")
        conn.commit()
        cur.close()
        conn.close()
        return "The Records have been Purged"
    else:
        try:
            cur.execute("DELETE FROM comments WHERE id=?", (identifier,))
            conn.commit()
            cur.close()
            conn.close()
            return "Deleted: %s" % identifier
        except Error as e:
            return "Could not delete %s" % e


def get_comments():
    comments = []
    results = []
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM comments")
        results = cur.fetchall()

    except Error as e:
        print "Error: %s" % e

    for result in results:
        comments.append(Comment(result[1], result[2], result[3], result[0]))

    return comments


# Comment Object
class Comment:

    def __init__(self, author, content, time_stamp=None, identifier=None):
        self.author = author
        self.content = content
        self.time_stamp = self.set_time_stamp(time_stamp)
        self.identifier = self.set_identifier(identifier)

    def get_content(self):
        return self.content

    def get_author(self):
        return self.author

    @staticmethod
    def set_time_stamp(time_stamp):
        if time_stamp is None:
            # creates time stamp of creation of the comment
            time = datetime.datetime.now().strftime("%m/%d/%y - %H:%M")

            return time
        else:
            return time_stamp


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
# TODO add a reply object, that is nearly identical to a comment, with an added
# paramerter, which is parent. Then create methods to get the replies. All replies must branch from a Comment or another reply.
# Create an sql table that will allow the loading and saving of these "replies"
