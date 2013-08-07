var webpage = require('webpage')
var system = require('system')

var socrata = (function(){
  var socrata = {}

  var email = system.env.SOCRATA_EMAIL
  var password = system.env.SOCRATA_PASSWORD

  if (typeof('email') === 'undefined' || typeof('password') === 'undefined'){
    console.log('Warning: SOCRATA_EMAIL or SOCRATA_PASSWORD might not be set.')
  }

  socrata.wait = function(sec, func) { setTimeout(func, sec * 1000) }

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
      domain = page.evaluate(function(email, password){
        document.querySelector('#user_session_login').value = email
        document.querySelector('#user_session_password').value = password
        document.querySelector('input[value="Sign In"]').click()
        return window.location.hostname
      }, email, password)
      socrata.wait(3, function(){
        page.render(domain + '-login.png')
        var user_name = page.evaluate(function(){
          return document.querySelector('.currentUser').innerText
        })
        if (user_name === 'Unknown User') {
          console.log('Logging in to ' + domain + ' failed.')
        } else if (callback) {
          callback(page)
        } else {
          console.log('No callback specified for ' + domain)
        }
      })
    })
  }

  socrata.nominate = function(page, title, description) {
    var domain = page.evaluate(function () {
      window.location.href = '/nominate'
      return window.location.hostname
    })
    socrata.wait(3, function(){
      page.render(domain + '-nominate.png')

      var can_nominate = page.evaluate(function(title, description){
        if (document.querySelector('#nominateTitle')) {
          // jQuery works but querySelector doesn't?
          jQuery('a[href="#Submit dataset"]').click()

          document.querySelector('#nominateTitle').value = title
          document.querySelector('#nominateDescription').value = description

          setTimeout(function(){
          // Do the submission.
          document.querySelector('a[href="#Submit"]').click()
          }, 1000)
          return true
        } else {
          return false
        }
      }, title, description)

      if (can_nominate) {
        socrata.wait(2, function(){
          page.render(domain + '-submit.png')
          console.log('Nominated the dataset on ' + domain)
        })
      } else {
        console.log('You cannot nominate datasets on ' + domain)
      }
    })
  }

  return socrata
})()


fs = require('fs')

TITLE = 'Data Portal Analytics'
DESCRIPTION = fs.read('description.txt')


var INTERVAL = 30
socrata.sites(function(sites){
  var total = sites.length
      so_far = 0

  for (i in sites) {
    socrata.wait(i * INTERVAL, function(){
      so_far++
      var site = sites.pop()

      console.log('\n' + site + ' (' + so_far + ' of ' + total + ')')
      var page = webpage.create()
      page.open('https://' + site + '/analytics', function(status) {
        if (null === page.plainText.match('Site Analytics')) {
          socrata.login(site, function(page){
            socrata.nominate(page, TITLE, DESCRIPTION)
          })
        } else {
          console.log(site + ' has already enabled the /analytics page.')
        }
      })
    })
  }
  socrata.wait(total * INTERVAL, phantom.exit)
})
