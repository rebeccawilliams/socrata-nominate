var socrata = (function(){
  var webpage = require('webpage')
  var socrata = {}

  socrata.is_domain = function(potential_url){
    return (null !== potential_url.match(/\./)) && (null == potential_url.match(/ /))
  }

  socrata.sites = function(callback) {
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
        return domain.replace('https://', '').replace('http://', '').replace(/\/$/, '')
      }).filter(function(domain) { return domain !== '' })
      callback(portals)
    })
  }

  socrata.login = function(site) {
    var page = webpage.create()
    page.open(url + '/login', function (status) {
      document.getElementById('user_session_login').value = 'abc'
      document.getElementById('user_session_password').value = 'abc'
      $('input[value="Sign In"]').click()
      console.log(window.location)
    })
  }

  socrata.nominate = function(site, title, description) {
    page.open(url + '/nominate', function (status) {
      $('a[href="#Submit dataset"]').click()
      phantom.exit()
    })
  }

  return socrata
})()

socrata.login('https://data.nola.gov')

/*
socrata.sites(function(sites){
  sites.map(function(site){
    console.log(site)
  })
})
*/
