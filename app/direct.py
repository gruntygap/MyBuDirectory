import mechanize
from app import app
from cookie import create_cookies

@app.route('/direct/<f_name>/<l_name>')
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