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


# Create Comment Object
class Comment:

    def __init__(self, name, post, time_stamp):
        self.name = name
        self.post = post
        self.time_stamp = time_stamp
        self.identifier = None
        
    def get_post(self):
        return self.post

    def get_name(self):
        return self.name

    def set_identifier(self):
        #Generates identifier

        self.identifier = 124
