upstream django_app {
    server django:8000;
}


log_format json escape=json '{ "time": "$time_iso8601", '
	'"remote_addr": "$remote_addr", '
	'"remote_user": "$remote_user", '
	'"ssl_protocol_cipher": "$ssl_protocol/$ssl_cipher", '
	'"body_bytes_sent": "$body_bytes_sent", '
	'"request_time": "$request_time", '
	'"status": "$status", '
	'"request": "$request", '
	'"request_method": "$request_method", '
	'"http_referrer": "$http_referer", '
	'"http_x_forwarded_for": "$http_x_forwarded_for", '
	'"http_cf_ray": "$http_cf_ray", '
	'"host": "$host", '
	'"server_name": "$server_name", '
	'"upstream_address": "$upstream_addr", '
	'"upstream_status": "$upstream_status", '
	'"upstream_response_time": "$upstream_response_time", '
	'"upstream_response_length": "$upstream_response_length", '
	'"upstream_cache_status": "$upstream_cache_status", '
	'"http_user_agent": "$http_user_agent" }';

server {

    listen 80;
    server_name localhost;
    # Redirect all HTTP traffic to HTTPS
    return 301 https://$host$request_uri;
}


server {

    listen 443 ssl;
    server_name localhost;
    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include /etc/nginx/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # gzip
    gzip on;
    gzip_vary on;
    gzip_proxied expired no-cache no-store private auth;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_min_length 2048;
    gzip_types
      application/atom+xml
      application/geo+json
      application/javascript
      application/x-javascript
      application/json
      application/ld+json
      application/manifest+json
      application/rdf+xml
      application/rss+xml
      application/xhtml+xml
      application/xml
      font/eot
      font/otf
      font/ttf
      image/svg+xml
      text/css
      text/javascript
      text/plain
      text/xml;

    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        autoindex off;
        proxy_pass http://django_app;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application

        # proxy_set_header Host $http_host;


        # proxy_set_header X-Forwarded-Host $server_name;

        # proxy_set_header Host $host;
        # proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        autoindex off;
        alias /opt/app/staticfiles/;
    }

    location /media/ {
        autoindex off;
        alias /opt/app/media/;
    }

   # path to proxy my WebSocket requests
   # location /ws/ {
   #       proxy_pass http://django_app; proxy_http_version 1.1;
   #       proxy_set_header Upgrade $http_upgrade;
   #       proxy_set_header Connection “upgrade”;
   #       proxy_redirect off;
   #       proxy_set_header Host $host;
   #       proxy_set_header X-Real-IP $remote_addr;
   #       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   #       proxy_set_header X-Forwarded-Host $server_name;
   #   }
}
