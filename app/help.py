from flask import render_template, request
from app import app
import smtplib
import os
import config


@app.route('/help', methods=['GET', 'POST'])
def help():
    sent = False
    if request.method == 'POST':
        sent = handle()
        if sent is True:
            return render_template('help.html', sent=sent)

    return render_template('help.html', sent=sent)


# Handles Post Request to the /help route
def handle():
    # form data
    data = request.form
    # message, name, email, type
    # Creates Message
    subject = 'SERVER CONTACT MESSAGE: %s by %s' % (data['type'], data['name'])
    message = 'Contact Email: %s \n' \
              'Contact Name: %s \n' \
              'Message: %s' % (data['email'], data['name'], data['message'])
    fromaddr = 'n3onsnak3@gmail.com'
    toaddrs = 'grant-gapinski@bethel.edu'
    msg = "\r\n".join([
        "From: n3onsnak3@gmail.com",
        "To: grant-gapinski@bethel.edu",
        "Subject: " + subject,
        "",
        message
    ])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    if config.testing:
        server.login(config.email_user, config.password)
    else:
        server.login(os.environ['email_user'], os.environ['password'])
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    return True
