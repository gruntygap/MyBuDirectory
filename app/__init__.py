from flask import Flask
from bs4 import BeautifulSoup
import requests
from requests import cookies
from twill.commands import *
import urllib2
import cookielib
import mechanize
from config import *

app = Flask(__name__)


# The link for scraping is: https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*
# https://auth.bethel.edu/cas/login
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/memes')
def lol():
    # Creating a cookie jar
    jar = requests.cookies.RequestsCookieJar()
    jar.set('CASTGC', 'TGT-288576-P2A5GpeI0HQmaqBGctFWWzM2i9SZQQObMFqg0BKh7Pd5YIdi22-auth.bethel.edu', domain='auth.bethel.edu', path='/cas/')
    jar.set('JSESSIONID', '595D542EA77366F75872EAA91958E2AE', domain='auth.bethel.edu', path='/cas')
    jar.set('__utma', '98157824.1888833403.1494529050.1501903865.1501903865.1', domain='.bethel.edu', path='/')
    jar.set('__utmz', '98157824.1501903865.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)', domain='.bethel.edu', path='/')
    jar.set('_ceg.s', 'ou70f0', domain='.bethel.edu', path='/')
    jar.set('_ceg.u', 'ou70f0', domain='.bethel.edu', path='/')
    jar.set('_ga', 'GA1.2.1888833403.1494529050', domain='.bethel.edu', path='/')
    jar.set('_gid', 'GA1.2.412462581.1504476722', domain='.bethel.edu', path='/')
    jar.set('optimizelyEndUserId', 'oeu1494529049786r0.11048882619692013', domain='.bethel.edu', path='/')
    jar.set('usid', '8+tZFCQlqATJBl6qQ5gHTg__', domain='.bethel.edu', path='/')
    # r = requests.get('https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*&ticket=ST-952494-vdYU5IAmvN4bkfyk7omU-auth.bethel.edu', cookies=jar, allow_redirects=False)
    # r = requests.get('https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*', cookies=jar)
    r = requests.post('https://directory.bethel.edu/cgi-bin/directory.cgi', cookies=jar, allow_redirects=False)
    # r = requests.get('https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*')
    r.history
    for resp in r.history:
        print resp.status_code, resp.url

    html_ingredients = '<meta http-equiv="Content-Security-Policy" content="script-src \'self\'">'
    html_ingredients += r.text
    soup = BeautifulSoup(html_ingredients, 'html.parser')
    print soup

    return soup.prettify()


# Gathers the Cookies for a selected webaddress form
# @app.route('/get-cookies')
def get_cookies():
    jar = cookielib.FileCookieJar("cookies")
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_cookiejar(jar)
    browser.open('https://auth.bethel.edu/cas/login')
    browser.select_form(nr=0)  # check yoursite forms to match the correct number
    browser['username'] = user # use the proper input type=text name
    browser['password'] = password  # use the proper input type=password name
    browser.submit()
    return jar


# Provides a Visual for the Cookies Gathered
@app.route('/get-cookies-view')
def get_cookies_view():
    jar = get_cookies()
    string = """
    <style>
        table, th, td {
            border: 1px solid black;    
            border-collapse: collapse;
        }
        th, td {
            padding: 15px;
        }
    </style>
    """
    string += 'Output: <i>Currently have %d cookies</i>' % len(jar)
    string += '<table>'
    for cookie in jar:
        string += '<tr>'
        string += '<th>'
        string += cookie.name
        string += '</th>'
        string += '<th>'
        string += cookie.value
        string += '</th>'
        string += '<th>'
        string += cookie.domain
        string += '</th>'
        string += '<th>'
        string += cookie.path
        string += '</th>'
        string += '</tr>'
    string += '</table>'
    return string


@app.route('/direct/<f_name>/<l_name>')
def direct(f_name, l_name):
    jar = get_cookies()
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    # Inserts Cookies
    browser.set_cookiejar(jar)
    browser.open(generate_url(f_name, l_name))
    browser.select_form(nr=0)
    response = browser.submit()
    # Returns HTML of Submit Response
    return response.read()


def generate_url(f_name, l_name):
    url = 'https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?'
    url += 'lname=' + l_name + '&fname=' + f_name + '&filter=Pictures&filter=Students'
    return url


def read_directory():
    pass
