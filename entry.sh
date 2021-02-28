#!/bin/bash

trap exit INT TERM

set -euxo pipefail

nginx -t
nginx

uwsgi --ini uwsgi.ini
