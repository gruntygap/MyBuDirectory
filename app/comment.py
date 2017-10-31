from flask import render_template
from app import app
import datetime
import uuid


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
    pass


def upload_comment(comment):
    author = comment.author
    content = comment.content
    time_stamp = comment.time_stamp
    id = comment.identifier

    pass


def delete_comment():
    pass


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
