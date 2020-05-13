#!/bin/bash

set -euxo pipefail

cp nginx.conf /conf/spass.conf

uwsgi --ini uwsgi.ini
