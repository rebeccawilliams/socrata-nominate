# vim: set fileencoding=utf-8
import re
import os
from requests import session
import lxml.html
import time
import json

def _parse_app_token(text):
    possibilities =  re.findall(r'blist\.configuration\.appToken="([^"]+)"', text)
    if len(possibilities) == 1:
        return possibilities[0]
    else:
        fp = open('/tmp/base.js', 'w')
        fp.write(text)
        fp.close()
        print possibilities
        raise ValueError("I couldn't find an app token. I'm writing the JavaScript file to \"/tmp/base.js\".")

def _parse_csrf_pair(text):
    'Get the CSRF token.'
    html = lxml.html.fromstring(text)
    csrf_param = unicode(html.xpath(u'//meta[@name="csrf-param"]/@content')[0])
    csrf_token = unicode(html.xpath(u'//meta[@name="csrf-token"]/@content')[0])
    return csrf_param, csrf_token

def _check_input(email, password):
    if email == None:
        if u'SOCRATA_EMAIL' in os.environ:
            email = os.environ[u'SOCRATA_EMAIL']
        else:
            raise ValueError(u'You must specify an email address.')

    if password == None:
        if u'SOCRATA_PASSWORD' in os.environ:
            password = os.environ[u'SOCRATA_PASSWORD']
        else:
            raise ValueError(u'You must specify a password.')

    return email, password

def _clean_portal_name(portal):
    u'Clean up the portal name'
    if not (portal.startswith(u'http://') or portal.startswith(u'https://')):
        # Add the protocal
        portal = u'https://' + portal
    if portal[-1] == u'/':
        # Remove trailing slash.
        portal = portal[:-1]
    return portal

class Session:
    def __init__(self, portal, email = None, password = None):
        u'Log in to the portal'
        # Check input
        email, password = _check_input(email, password)
        self.portal = _clean_portal_name(portal)

        # Start the web session
        self.session = session()

        # Log in
        response = self.session.get(self.portal + u'/login')
        csrf_param, csrf_token = _parse_csrf_pair(response.text)
        self.session.post(self.portal + u'/user_sessions', data = {
            u'utf8': u'✓',
            csrf_param: csrf_token,
            u'user_session[login]': email,
            u'user_session[password]': password,
            u'commit': u'Sign In',
        })

        # Set the app token.
        cachebuster = int(time.time())
        response = self.session.get(self.portal + u'/packages/base.js?%d' % cachebuster)
        self.app_token = _parse_app_token(response.text)

    def nominate(self, title, description):
        u'Nominate a dataset.'

        # Get CSRF pair
        url = portal + u'/nominate'
        response = self.session.get(url)
        _, csrf_token = self.get_csrf_pair(response)

        # Submit the dataset
        url = portal + u'/api/nominations?accessType=WEBSITE'
        data = json.dumps({
            u'description': description,
            u'title': title,
        })
        headers = {
            u'Content-type': u'application/json',
            u'X-App-Token': self.app_token,
            u'X-CSRF-Token': csrf_token,
            u'X-Requested-With': u'XMLHttpRequest',
            u'X-Socrata-Federation': u'Honey Badger',
        }
        response = self.session.post(url, data = data, headers = headers)
