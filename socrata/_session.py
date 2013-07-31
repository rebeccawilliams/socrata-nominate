# vim: set fileencoding=utf-8
import os
from requests import session
import lxml.html

class Session:
    def __init__(self, portal, email = None, password = None):
        u'Log in to the portal'

        # Check input
        if email == None:
            if u'SOCRATA_EMAIL' in os.environ:
                email = os.environ[u'SOCRATA_EMAIL']
            else:
                raise ValueError('You must specify an email address.')
        elif password == None:
            if u'SOCRATA_PASSWORD' in os.environ:
                password = os.environ[u'SOCRATA_PASSWORD']
            else:
                raise ValueError('You must specify a password.')

        # Clean up the portal name
        if not (portal.startswith('http://') or portal.startswith('https://')):
            # Add the protocal
            portal = 'https://' + portal
        if portal[-1] == u'/':
            # Remove trailing slash.
            portal = portal[:-1]
        self.portal = portal

        # Start the web session
        self.session = session()

        # Log in
        response = self.session.get(self.portal + u'/login')
        html = lxml.html.fromstring(response.text)
        # Get the CSRF token
        # <meta content="authenticity_token" name="csrf-param" />
        # <meta content="CR0tPy8mxG/qancEuJlguBlUVwZWEAKw7RWLWcCPWTM=" name="csrf-token" />
        csrf_param = unicode(html.xpath(u'//meta[@name="csrf-param"]/@content')[0])
        csrf_token = unicode(html.xpath(u'//meta[@name="csrf-token"]/@content')[0])
        self.session.post(self.portal + u'/user_sessions', data = {
            u'utf8': u'✓',
            csrf_param: csrf_token,
            u'user_session[login]': email,
            u'user_session[password]': password,
            u'commit': u'Sign In',
        })
