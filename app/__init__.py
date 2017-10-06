from flask import Flask, render_template
from bs4 import BeautifulSoup
import mechanize
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


@app.route('/read-gstyle/<f_name>/<l_name>')
def parse_directory_html(f_name,l_name):
    html = direct(f_name, l_name)
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

                    # gets the actual photo link, not the <img> tag
                    if photo_link is None:
                        # Do nothing
                        photo_link = "None"
                    else:
                        photo_link = photo_link['src']

                    # Takes the second <td> cell which holds Name, Email, Dorm, PO
                    info_td = pos_image.find_next('td')
                    info_name = info_td.find_next('b').get_text()
                    pos_email = info_td.find('a')

                    # if there is an email that is not equal to none
                    # then set the email var
                    if pos_email is not None:
                        info_email = pos_email.get_text()
                    else:
                        info_email = None

                    extra_info = info_td.next_sibiling

                    # Returning Data #
                    # Cell is a person input info
                    print "*-" * 25, "INPUT DATA", "-*" * 25
                    print "General info: %s" % info_td
                    print "Name:", info_name
                    print "E-Mail:", info_email
                    print "Extra Info?:", extra_info
                    print "Photo link: %s" % photo_link
                    print ""

                    strn += "<h3> INPUT DATA </h3>"
                    strn += "<p>General info: %s </p>" % info_td
                    strn += "<p>Name: %s </p>" % info_name
                    strn += "<p>E-Mail: %s </p>" % info_email
                    strn += "<p>Extra Info: %s </p>" % extra_info
                    strn += "<p>Photo Link: %s </p>" % photo_link
    return strn
