from flask import render_template
from app import app


@app.route('/comments')
def comments():
    # TODO Load comments once feature is added
    return render_template('comments.html')


@app.route('/comments/new')
def new_comment():
    return render_template('newCommentForm.html')


def delete_comment():
    pass


# Comment Object
class Comment:

    def __init__(self, name, content, time_stamp):
        self.name = name
        self.content = content
        self.time_stamp = self.set_time_stamp()
        self.identifier = self.set_identifier()

    def get_content(self):
        return self.content

    def get_name(self):
        return self.name

    def set_identifier(self):
        # Generates identifier

        self.identifier = 124

        return 1

    def set_time_stamp(self):

        self.name = 5
        return 1
