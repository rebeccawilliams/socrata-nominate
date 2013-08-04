var socrata = (function(){
  var webpage = require('webpage')
  var system = require('system')
  var socrata = {}

  var email = system.env.SOCRATA_EMAIL
  var password = system.env.SOCRATA_PASSWORD

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

  socrata.login = function(domain, callback) {
    var page = webpage.create()
    page.open('https://' + domain + '/login', function (status) {
      var x = page.evaluate(function(email, password){
        document.querySelector('#user_session_login').value = email
        document.querySelector('#user_session_password').value = password
        document.querySelector('input[value="Sign In"]').click()
      }, email, password)
      setTimeout(function(){
        page.render('login.png')
        var user_name = page.evaluate(function(){
          return document.querySelector('.currentUser').innerText
        })
        if (user_name === 'Unknown User') {
          console.log('Logging in failed.')
          phantom.exit()
        } else if (callback) {
          callback(page)
        } else {
          phantom.exit()
        }
      }, 3000)
    })
  }

  socrata.nominate = function(page, title, description) {
    page.evaluate(function () {
      window.location.href = '/nominate'
    })
    setTimeout(function(){
      page.render('nominate.png')

      // $('a[href="#Submit dataset"]').click()
      phantom.exit()

    }, 3000)
  }

  return socrata
})()

socrata.login('data.nola.gov', function(page){
  socrata.nominate(page, 'a', 'b')
})

/*
socrata.sites(function(sites){
  sites.map(function(site){
    console.log(site)
  })
})
*/
