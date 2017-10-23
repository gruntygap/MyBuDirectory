from flask import render_template
from app import app


@app.route('/comments')
def comments():
    return render_template('comments.html')
