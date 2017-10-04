import cookielib
import mechanize
from flask import render_template
# Local
from config import *
from app import app


# Gathers the Cookies for a selected webaddress form
# @app.route('/get-cookies')
def create_cookies():
    jar = cookielib.FileCookieJar("cookies")
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_cookiejar(jar)
    browser.open('https://auth.bethel.edu/cas/login')
    browser.select_form(nr=0)  # check yoursite forms to match the correct number
    browser['username'] = user  # use the proper input type=text name
    browser['password'] = password  # use the proper input type=password name
    browser.submit()
    return jar


# def try_cookies(jar):
#     for cookie in jar:
#         if cookie.isExpired():
#             print "We made new cookies"
#             create_cookies()
#         else:
#             print "No new cookies"

# Provides a Visual for the Cookies Gathered
@app.route('/get-cookies-view')
def get_cookies_view():
    jar = create_cookies()
    # How one would access them via python
    # for cookie in jar:
    #     cookie.name
    #     cookie.value
    #     cookie.domain
    #     cookie.path
    return render_template('cookie_view.html', **locals())
