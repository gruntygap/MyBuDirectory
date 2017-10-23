from flask import render_template, request
from app import app
import smtplib


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
    username = 'n3onsnak3@gmail.com'
    password = 'Technology'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    return True
