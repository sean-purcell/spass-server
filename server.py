#!/usr/bin/python3

import subprocess

from flask import Flask

app = Flask(__name__)

def call_spass(name, master):
    subprocess.Popen(

@app.route('/getpwd', methods=['POST'])
def getpwd():
    
