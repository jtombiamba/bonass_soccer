#!/bin/sh

set -e

echo "GETTING CERTIFICATE"


certbot certonly \
  --webroot \
  -w /etc/letsencrypt \
  -d tombislab.com -d www.tombislab.com \
  --email tombisales@gmail.com --agree-tos --no-eff-email