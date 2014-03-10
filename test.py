#/usr/bin/env python

from requests import get, post, Session
import common
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

def url(x):
    return 'http://localhost:{}/{}'.format(common.SERVER_PORT, x)

def assert_response(resp, comp, status=200, f=lambda x:x.text):
    assert resp.status_code == status, "Status is {}".format(resp.status_code)
    if comp is not None:
        v = f(resp)
        assert v == comp, "Result is {}".format(v)

def test_login_logout():
    s = Session()
    rt = s.get(url('fl'))
    assert_response(rt, 'Login OK')
    rt = s.get(url('whoami'))
    assert_response(rt, common.FAKE_USER)
    s.get(url('logout'))
    rt = s.get(url('whoami'))
    assert_response(rt, None, status=401)
               
def test_version():
    rt = get(url('v'))
    assert_response(rt, common.VERSION, f=lambda x:x.json()['version'])
