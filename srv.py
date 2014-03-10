#/usr/bin/env python

from flask import request, g, Flask, session

from json import dumps

from common import VERSION, DEBUG, FAKE_USER, SERVER_PORT,\
    jsonfunc, userfunc, debugfunc, prepare_logging

from debugbp import debug_routes

app = Flask(__name__)

logger = prepare_logging(name=__name__)

@app.route('/logout')
@userfunc
def logout():
    del session['user']
    session.modified = True
    return ''


if __name__ == '__main__':
    app.secret_key = 'FIXME: Replace with anything `date | md5sum`'
    if DEBUG:
        app.register_blueprint(debug_routes)
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=DEBUG)
