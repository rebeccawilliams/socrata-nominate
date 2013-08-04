var socrata = (function(){
  var webpage = require('webpage')
  var socrata = {}

  socrata.is_domain = function(potential_url){
    return (null !== potential_url.match(/\./)) && (null == potential_url.match(/ /))
  }

  socrata.sites = function() {
    var page = webpage.create()
    page.open('http://status.socrata.com/sites', function(status) {
      console.log(page.plainText)
    })
  }
      /*
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
      */

  /*
  socrata.nominate = function(site, title, description) {
    var page = require('webpage').create()
    page.open(url, function (status) {
      phantom.exit()
    })
  }
  */
  return socrata
})()

socrata.sites()
