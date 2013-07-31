import nose.tools as n
import socrata._session as session

def test_parse_app_token():
    'The app token should be parsed from the minified JavaScript.'
    observed = session._parse_app_token('''nce_message&&window==window.top&&$.cookies.get("maintenance_ack")!=blist.configuration.maintenance_hash){var c=function(){$("#maintenanceNotice").fadeOut()};$("#siteHeader").after(blist.configuration.maintenance_message);setTimeout(c,15000);$("#maintenanceNotice a.close").click(function(k){k.preventDefault();c();$.cookies.set("maintenance_ack",blist.configuration.maintenance_hash)})}var f=$('meta[name="csrf-token"]').attr("content");if(!$.isBlank(f)){$.cookies.set("socrata-csrf-token",f)}blist.configuration.appToken="U29jcmF0YS0td2VraWNrYXNz0";$.ajaxSetup({beforeSend:function(k){k.setRequestHeader("X-App-Token",blist.configuration.appToken);k.setRequestHeader("X-CSRF-Token",f)}});$(".dateReplace").each(function(){var l=$(this);var k;switch(l.data("dateformat")){case"date_time":k="M d, Y g:ia";break;case"long_date":k="F d, Y";break;case"date":default:k="M d, Y";break}l.text(new Date(l.data("rawdatetime")*1000).format(k))});var e=[];var h=[];var g=false;var b=function(m,k){for(var l=0;l<m.length;l++){successCallback=m[l];if(_.isFunction(successCallback)){successCallback(k)}}};var a=function(){$.socrataServer.makeRequest({type:"GET",url:"/api/users/current.json",headers:{"Cache-Control":"nocache"},success:function(k){g=true;k=new User(k);blist.currentUser=k;blist.currentUserId=k.id;var l=e.concat(h);b(l,k)},error:function(){g=true;b(h)}})};var j=$.cookies.get("logged_in");if(j&&j=="true"&&blist.currentUser===undefined){a()}else{g=true;b(h,blist.currentUser)}blist.configuration.onCurrentUser=function(k){if(blist.currentUser!==undefined){k(blist.currentUser)}else{e.push(k)}};blist.configuration.onCurrentUserComplete=function(k){if(g){k(blist.currentUser)}else{h.push(k)}};blist.configuration.onCu''')
    expected = u'U29jcmF0YS0td2VraWNrYXNz0'
    n.assert_equal(observed, expected)

def test_parse_csrf_pair():
    observed = session._parse_csrf_pair('''
    <html>
      <meta content="authenticity_token" name="csrf-param" />
      <meta content="CR0tPy8mxG/qancEuJlguBlUVwZWEAKw7RWLWcCPWTM=" name="csrf-token" />
    </html>
    ''')
    expected = (u'authenticity_token', u'CR0tPy8mxG/qancEuJlguBlUVwZWEAKw7RWLWcCPWTM=')
    n.assert_tuple_equal(observed, expected)

def check_check_input(email_env, password_env, email_in, password_in, email_out, password_out):
    if email_env == None:
        if u'SOCRATA_EMAIL' in session.os.environ:
            del session.os.environ[u'SOCRATA_EMAIL']
    else:
        session.os.environ[u'SOCRATA_EMAIL'] = email_env

    if password_env == None:
        if u'SOCRATA_PASSWORD' in session.os.environ:
            del session.os.environ[u'SOCRATA_PASSWORD']
    else:
        session.os.environ[u'SOCRATA_PASSWORD'] = password_env

    email_observed, password_observed = session._check_input(email_in, password_in)
    if email_env == email_in == None:
        n.assert_raises(ValueError, lambda: session._check_input(email_in, password_in))
    elif password_env == password_in == None:
        n.assert_raises(ValueError, lambda: session._check_input(email_in, password_in))
    else:
        n.assert_equal(email_observed, email_out)
        n.assert_equal(password_observed, password_out)

def test_check_input():
    yield check_check_input, u'tom@example.com', u'abc', None, None, u'tom@example.com', u'abc'
    yield check_check_input, u'bob@example.com', u'abc', u'tom@example.com', None, u'tom@example.com', u'abc'
    yield check_check_input, u'tom@example.com', None, None, u'abc', u'tom@example.com', u'abc'
    yield check_check_input, u'tom@example.com', u'abc', None, None, u'tom@example.com', u'abc'
    yield check_check_input, u'tom@example.com', None, None, None, u'tom@example.com', u'abc'
