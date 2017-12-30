#!/usr/bin/python3

import logging
import subprocess
import sys

from flask import Flask, request

app = Flask(__name__)

SPASS=sys.argv[1] if len(sys.argv) > 1 else 'spass'
DBFILE=sys.argv[2] if len(sys.argv) > 2 else ''

COMMAND = [SPASS, '-s'] + (['-d', DBFILE] if DBFILE else [])

@app.before_first_request
def setup():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

def call_spass(stdin, cmd):
    cmdline = COMMAND + cmd
    p = subprocess.Popen(cmdline,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    try:
        out, err = p.communicate(bytes('%s\n' % stdin, 'utf8'), timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
        return 'Error: spass process timedout'

    return out + err, p.returncode

@app.route('/get', methods=['POST'])
def get():
    val, code = call_spass(request.form['master'], ['get',
        request.form['name']])
    app.logger.info('get: %s %s %d', request.remote_addr, request.form['name'], code)
    return val

@app.route('/ls', methods=['POST'])
def ls():
    val, code = call_spass(request.form['master'], ['ls'])
    app.logger.info('ls: %s %d', request.remote_addr, code)
    return val.replace(b'\n', b'<br/>')

@app.route('/gen', methods=['POST'])
def gen():
    print(request.form)
    def C(name):
        return 'y' if request.form[name] == 'on' else 'n'
    val, code = call_spass(
        '%s' % (request.form['master']),
        ['gen', request.form['name'],
            '-l', request.form['length'],
            '-a', C('lower'),
            '-A', C('upper'),
            '-0', C('digit'),
            '-@', C('sym')])
    app.logger.info('gen: %s %s %d', request.remote_addr, request.form['name'], code)
    return val.replace(b'\n', b'<br/>')

@app.route('/add', methods=['POST'])
def add():
    val, code = call_spass(
        '%s\n%s\n%s' % (request.form['master'], request.form['password'],
            request.form['confirm']),
        ['add', request.form['name']])
    app.logger.info('add: %s %s %d', request.remote_addr, request.form['name'], code)
    return val

@app.route('/rm', methods=['POST'])
def rm():
    val, code = call_spass(
        '%s' % (request.form['master']),
        ['rm', request.form['name']])
    app.logger.info('rm: %s %s %d', request.remote_addr, request.form['name'], code)
    return val

@app.route('/chpw', methods=['POST'])
def chpw():
    val, code = call_spass(
        '%s\n%s\n%s' % (request.form['master'], request.form['newmaster'],
            request.form['confirm']),
        ['chpw'])
    app.logger.info('chpw: %s %d', request.remote_addr, code)
    return val

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
