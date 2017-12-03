#!/usr/bin/python3

import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)

SPASS='/usr/local/bin/spass'

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

    return out if p.returncode == 0 else err

@app.route('/getpwd', methods=['POST'])
def getpwd():
    return call_spass(request.form['name'], request.form['master'])

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        SPASS = sys.argv[1]
    app.run()
