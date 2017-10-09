from flask import Flask, render_template

# not being used
# import requests
# from requests import cookies
# from twill.commands import *
# import urllib2
# import cookielib

app = Flask(__name__)
from app import cookie
from direct import direct


# The link for scraping is: https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*
# https://auth.bethel.edu/cas/login
@app.route('/')
def hello_world():
    return render_template('index.html')
