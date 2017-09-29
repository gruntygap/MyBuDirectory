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
    return 'Long Ding Dong'


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
    # Returns HTML of Submit Response
    response = browser.submit()
    return response.read()


def generate_url(f_name, l_name):
    gen_url = 'https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?'
    # gen_url += 'lname=' + l_name + '&fname=' + f_name + '&filter=Pictures&filter=Students'
    gen_url += 'lname=' + l_name + '&fname=' + f_name + '&filter=Pictures'
    return gen_url


@app.route('/read-gstyle')
def parse_directory_html():
    html = direct('*', '*')
    soup = BeautifulSoup(html, 'html.parser')
    initial_p = soup.p.string
    strn = ''
    if initial_p == 'Too many entries matched your search; please narrow it down.':
        # Read print statments
        print "There is nothing to search here: Too many Entries"

    elif initial_p == 'No entries matched your search.':
        # Read print statments
        print "There is nothing to search here: No Entries"

    else:
        # Read print statments
        print "duuuuude we searchin"

        for h3 in soup.find_all('h3'):
            if h3.string == 'Students':
                table = h3.find_next('table')
                # Searches through Table Rows
                for cell in table.find_all('tr'):
                    # TODO create a person object with data:
                        # TODO person(first_name, last_name, email, photofile, dorm, PO)
                    # Taking the initial <td> cell, which possibly contains a <img tag>
                    pos_image = cell.find_next('td')
                    # if there is a photo link within pos_image, the <img> tag is stored.
                    photo_link = pos_image.find('img')
                    # Takes the second <td> cell which holds Name, Email, Dorm, PO
                    info_td = pos_image.find_next('td')
                    info_name = info_td.find_next('b').get_text()
                    pos_email = info_td.find('a')

                    # if there is an email that is not equal to none
                    # then set the email var
                    if(pos_email != None):
                        info_email = pos_email.get_text()
                    else:
                        info_email = None

                    extra_info = info_td.find("br")

                    # Cell is a person input info
                    print "*-" * 25, "INPUT DATA", "-*" * 25
                    print "General info: %s" % info_td
                    print "Name:", info_name
                    print "E-Mail:", info_email
                    print "Extra Info?:", extra_info
                    print "Photo link: %s" % photo_link
                    print ""


        # TODO perhaps search via an itteration of the tables and table elements, identify the tables
            # with the h3 headers.
    return strn
