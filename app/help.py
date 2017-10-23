from flask import render_template, request
from app import app
import smtplib


@app.route('/help', methods=['GET', 'POST'])
def help():
    if request.method == 'POST':
        handle()

    return render_template('help.html')


def handle():
    # form data
    data = request.form
    # message, name, email
    # TODO get mail working
    msg = data['message']
    server = smtplib.SMTP('localhost')
    server.sendmail('sender@example.com', 'grant-gapinski@bethel.edu', msg)
    server.quit()
    print data['message']
