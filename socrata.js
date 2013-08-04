(function(){
  module.exports = {}

  module.exports.is_domain = function(potential_url){
    return (null !== potential_url.match(/\./)) && (null == potential_url.match(/ /))
  }

  module.exports.sites = function() {
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
  }
  module.exports.nominate = function(site, title, description) {
    var page = require('webpage').create()
    page.open(url, function (status) {
      phantom.exit();
    })
  }
})
