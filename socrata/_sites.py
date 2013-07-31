import os, json, warnings
from urllib2 import urlopen, HTTPError

def is_domain(potential_url):
    return '.' in potential_url and ' ' not in potential_url

def sites():
    handle = urlopen('http://status.socrata.com/sites')
    portals = json.load(handle)
    for portal in portals:
        if is_domain(portal['description']):
            domain = portal['description']
        elif is_domain(portal['name']):
            domain = portal['name']
        elif portal['name'] == 'Socrata':
            continue
        else:
            warnings.warn('Could not find a valid domain for %s, skipping' % portal['name'])
            continue

        domain = domain.replace('https://', '').replace('http://', '')
        yield domain
