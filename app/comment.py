from flask import render_template
from app import app


@app.route('/comments')
def comments():
    return render_template('comments.html')


@app.route('/comments/new')
def create_comment():
    return render_template('newCommentForm.html')
