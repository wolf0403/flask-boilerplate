#!/usr/bin/env python

from __future__ import unicode_literals, print_function
import logging
from json import dumps

from flask import Response, session

SERVER_PORT = 8888


FAKE_USER = 'FAKE_USER'

_DEFAULT_LOGGING_CONFIG = {
    'level': logging.DEBUG,
}

def prepare_logging(**kw):
    cfg = dict(_DEFAULT_LOGGING_CONFIG.items() + kw.items())
    logging.basicConfig(**cfg)
    name = kw.get('name', __name__)
    l = logging.getLogger(name)
    return l

logger = prepare_logging()

from functools import wraps
def jsonfunc(f):
    def filtdict(d, *p, **kw):
        '''Potential filter for JSON structs'''
        return d # nothing to filter ATM
    
    def return_obj(d):
        if type(d) in [list, dict]:
            d = filtdict(d)
        return dumps(d)
    
    @wraps(f)
    def wrapper(*a, **kw):
        r = None
        status = 200
        try:
            r = f(*a, **kw)
            if isinstance(r, tuple):
                # WSGI response format, non-200 status
                r, status = r
                assert isinstance(status, int)
            if isinstance(r, Response):
                return r
            rtstr = return_obj(r)
            headers = {b'Content-Type':b'application/json'}
            if rtstr:
                return Response(rtstr, status, headers)
            if rtstr is None:
                status = 404
            return Response(rtstr, status, headers)
        except AssertionError as e:
            logger.exception('Assertion Error ' + str(e))
            raise
        except Exception as e:
            logger.exception('Returning JSON failed')
            raise e # Let Flask handle it

    return wrapper

def userfunc(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if 'user' in session:
            u = session['user']
            logger.debug('User %s calling %s', u, str(f))
            return f(*a, **kw)
        return Response('User not logged in', status=401)
    return wrapper

def debugfunc(f):
    '''Interfaces that only valid if common.DEBUG is set'''
    @wraps(f)
    def wrapper(*a, **kw):
        if DEBUG == True:
            return f(*a, **kw)
        return Response('', status=404)
    return wrapper
