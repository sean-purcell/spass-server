#!/usr/bin/python3

import logging
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)

SPASS=sys.argv[1] if len(sys.argv) > 1 else '/usr/local/bin/spass'

@app.before_first_request
def setup():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

def call_spass(name, master):
    p = subprocess.Popen([
            SPASS,
            'get',
            name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    try:
        out, err = p.communicate(bytes('%s\n' % master, 'utf8'), timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
        return 'Error: spass process timedout'

    return (out if p.returncode == 0 else err), p.returncode

@app.route('/getpwd', methods=['POST'])
def getpwd():
    val, code = call_spass(request.form['name'], request.form['master'])
    app.logger.info('%s %s %d', request.remote_addr, request.form['name'], code)
    return val

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
