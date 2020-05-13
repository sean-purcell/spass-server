#!/bin/bash

set -euxo pipefail

mkdir -p /www/spass
cp index.html /www/spass
cp nginx.conf /conf/spass.conf

uwsgi --ini uwsgi.ini
