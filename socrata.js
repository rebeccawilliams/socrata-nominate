var socrata = (function(){
  var webpage = require('webpage')
  var socrata = {}

  socrata.is_domain = function(potential_url){
    return (null !== potential_url.match(/\./)) && (null == potential_url.match(/ /))
  }

  socrata.sites = function() {
    var page = webpage.create()
    page.open('http://status.socrata.com/sites', function(status) {
      var portals = JSON.parse(page.plainText).map(function(portal){
        if (socrata.is_domain(portal.description)) {
          var domain = portal.description
        } else if (socrata.is_domain(portal.name)) {
          var domain = portal.name
        } else {
          var domain = ''
        }
        return domain.replace('https://', '').replace('http://', '')
      }).filter(function(domain) { return domain !== '' })
      console.log(portals)
    })
  }

  socrata.nominate = function(site, title, description) {
    webpage.create()
    page.open(url, function (status) {
      phantom.exit()
    })
  }
  return socrata
})()

socrata.sites()
