#!/usr/bin/env python
#
# Copyright (C) 2013 Alfredo Torre
# Released under MIT license, see LICENSE
#
# The following users are already available:
#  admin/admin, demo/demo

import bottle
from bottle import template, static_file, request
from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend
import logging


logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('cork_conf', email_sender='user@email.com', smtp_url='smtp://smtp.email.com')

# Populate Backend
def populate_backend():
    log.debug("Populate")
    b = SQLiteBackend('example.sqlite', initialize=True)
    b.connection.executescript("""
        INSERT INTO users (username, email_addr, desc, role, hash, creation_date) VALUES
        (
            'admin',
            'admin@localhost.local',
            'admin test user',
            'admin',
            'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=',
            '2012-10-28 20:50:26.286723'
        );
        INSERT INTO roles (role, level) VALUES ('special', 200);
        INSERT INTO roles (role, level) VALUES ('admin', 100);
        INSERT INTO roles (role, level) VALUES ('editor', 60);
        INSERT INTO roles (role, level) VALUES ('user', 50);
    """)
    return b

b = populate_backend()
aaa = Cork(backend=b, email_sender='user@email.com', smtp_url='smtp://smtp.email.com')


app = bottle.app()
# Beaker configuration 
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)

## Bottle routes ##

@bottle.route('/')
@bottle.view('index')
def index():
    """Only authenticated users can access the index page of the application"""
    aaa.require(fail_redirect='/login')
    return {'title': 'Index page', 'user': aaa.current_user.username, 'content': 'Index page\'s content'}


@bottle.post('/login')
def login():
    """User authentication"""
    username = request.forms.get('username')
    password = request.forms.get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/login')

@bottle.post('/register')
def register():
    """Send out registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    return 'Please check your mailbox.'


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address')
    )
    return 'Please check your mailbox.'


@bottle.route('/change_password/:reset_code')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'

@bottle.route('/restricted_download')
def restricted_download():
    """Only authenticated users can download this file"""
    aaa.require(fail_redirect='/login')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print "Session from simple_webapp", repr(session)
    
    aaa.require(fail_redirect='/login')
    return aaa.current_user.role


# Admin-only pages

@bottle.route('/admin')
@bottle.view('admin')
def admin():
    """Only admin users can see this"""
    aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        title="Admin page",    
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles()
    )


@bottle.post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)




# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

@bottle.route('/assets/<file:path>')
def assets(file):
    return static_file(file, root='./assets')

## Errors

@bottle.error(404)
def error404(error):
    return 'Nothing here, sorry --!'

##  Web app main  ##

def main():
    # Start the Bottle webapp
    bottle.run(app=app, quiet=False, reloader=False, debug=True)

if __name__ == "__main__":
    main()
