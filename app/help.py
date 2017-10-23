from flask import render_template
from app import app


@app.route('/help')
def help():
    return render_template('help.html')
