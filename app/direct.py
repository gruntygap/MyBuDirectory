from flask import render_template
import mechanize
from app import app
from cookie import create_cookies
from bs4 import BeautifulSoup
from Person import *


@app.route('/direct')
def main_direct():
    return render_template('direct.html')


@app.route('/direct-old/<f_name>/<l_name>')
def direct(f_name, l_name):
    jar = create_cookies()
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

# The link for scraping is: https://directory.bethel.edu/cgi-bin/sso/dirsso.cgi?lname=*&fname=*
# https://auth.bethel.edu/cas/login
@app.route('/direct/<f_name>/<l_name>')
def parse_directory_html(f_name, l_name):
    html = direct(f_name, l_name)
    soup = BeautifulSoup(html, 'html.parser')
    initial_p = soup.p.string
    strn = ''
    people = []
    if initial_p == 'Too many entries matched your search; please narrow it down.':
        # Read print statments
        print "Too many Entries"
        strn += '<div class="alert alert-danger" role="alert"><strong>There is nothing to search here:</strong> Too many Entries</div>'

    elif initial_p == 'No entries matched your search.':
        # Read print statments
        print "There is nothing to search here: No Entries"
        strn += '<div class="alert alert-danger" role="alert"><strong>There is nothing to search here:</strong> NO Entries</div>'

    else:
        # Creates an Array of people
        print "performed search on: %s, %s" % (f_name, l_name)
        for h3 in soup.find_all('h3'):
            if h3.string == 'Students':
                table = h3.find_next('table')
                # Searches through Table Rows
                for cell in table.find_all('tr'):
                    # Taking the initial <td> cell, which possibly contains a <img tag>
                    pos_image = cell.find_next('td')
                    # if there is a photo link within pos_image, the <img> tag is stored.
                    photo_link = pos_image.find('img')

                    # gets the actual photo link, not the <img> tag
                    if photo_link is None:
                        # Do nothing
                        photo_link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Nicolas_Cage_2011_CC.jpg/220px-Nicolas_Cage_2011_CC.jpg'
                    else:
                        photo_link = photo_link['src']

                    # Takes the second <td> cell which holds Name, Email, Dorm, PO
                    info_td = pos_image.find_next('td')
                    info_name = info_td.find_next('b').get_text()
                    # Removes the Name
                    info_td.b.decompose()
                    pos_email = info_td.find('a')

                    # if there is an email that is not equal to none
                    # then set the email var
                    if pos_email is not None:
                        info_email = pos_email.get_text()
                        # removes the E-mail
                        info_td.a.decompose()
                    else:
                        info_email = None

                    # Finding the Info (Place, PO, (ID?))
                    info_po = None
                    info_place = None
                    for child in info_td.strings:
                        # Pulls the PO number out
                        if 'PO# ' in child:
                            info_po = int(child.replace('PO# ', ''))
                        if 'Hall' in child or 'St.' in child or 'Arden' in child or 'Apartments' in child or 'San' in child:
                            info_place = child

                    # Returning Data #
                    # Cell is a person input info
                    # print "*-" * 25, "INPUT DATA", "-*" * 25
                    # print "General info: %s" % info_td
                    # print "Name:", info_name
                    # print "E-Mail:", info_email
                    # print "Photo link: %s" % photo_link
                    # print ""
                    person = Person(info_name, info_email, photo_link, info_po, info_place)
                    # add person to the array
                    people.append(person)
    # The Amount of People in the Array
    found = people.__len__()
    print "%s people found" % found
    return render_template('cards.html', people=people, strn=strn, found=found)
