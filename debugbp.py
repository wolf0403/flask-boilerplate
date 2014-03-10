#/usr/bin/env python

from flask import request, g, Flask, session, Blueprint
from common import *

debug_routes = Blueprint('debug_routes', __name__)

@debug_routes.route('/v')
@jsonfunc
def v():
    return {'version': VERSION}

@debug_routes.route('/fl')
@debugfunc
def fake_login():
    session.new = True
    session['user'] = FAKE_USER
    session.modified = True
    return 'Login OK'

@debug_routes.route('/whoami')
@userfunc
@debugfunc
def whoami():
    return session['user']

                         
