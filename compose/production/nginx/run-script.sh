#!/bin/bash

set -e

export host=\$host
export request_uri=\$request_uri

envsubst < /etc/nginx/conf.d/nginx.conf.tpl > /etc/nginx/conf.d/nginx.conf