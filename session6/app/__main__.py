#!/usr/bin/env python3

import os
import sys
import random
from logging import (debug, info, warning, error, critical,
                     basicConfig, INFO)
from flask import (Flask, request, Response, render_template, url_for,
                   make_response)

basicConfig(stream=sys.stderr, level=INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Application parameters
BIND_ADDR = '0.0.0.0'
if os.environ.get('DEBUG').lower() in ('y', 'yes', '1', 'true'): DEBUG=True
else                                                           : DEBUG=False
try:
    BIND_PORT = int(os.environ.get('BIND_PORT', 5001))
except ValueError:
    BIND_PORT = 5001

# Create Flask instance
app = Flask(__name__, template_folder='t')

@app.route('/meta-data')
def meta_data():
    debug('arguments: %s' % list(request.args))
    debug('host: %s' % request.host)
    debug('user_agent: %s' % request.user_agent)
    debug('remote_addr: %s')
    templ_vars = {
        'fqdn'          : 'host%d.example.com' % random.randint(100, 9999),
        'loghost_url'   : '169.254.169.254:514',
        'phone_home_url': 'http://169.254.169.254:5001/phone_home',
    }
    resp = make_response(render_template('meta-data.j2', **templ_vars))
    resp.headers['Content-Type'] = 'text/yaml'
    return resp

@app.route('/user-data')
def user_data():
    debug('arguments: %s' % list(request.args))
    debug('host: %s' % request.host)
    debug('user_agent: %s' % request.user_agent)
    debug('remote_addr: %s')
    resp = make_response(render_template('user-data.j2'))
    resp.headers['Content-Type'] = 'text/yaml'
    return resp

@app.errorhandler(404)
def page_not_found(e):
    return e

@app.route('/phone_home', methods=['POST', 'GET'])
def phone_home():
    r'''Process phone_home requests, e.g.:
    curl --data instance-id=23423423 \
        http://169.254.169.254:5001/phone_home
    '''
    if request.method == 'POST':
        return str(  [ (k,v) for k,v in request.form.items() ] )
    else:
        return phone_home.__doc__

if __name__ == '__main__':
    app.run(host=BIND_ADDR, port=BIND_PORT, debug=DEBUG)
