upstream django_app {
    server django:8000;
}

server {

    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        try_files $uri @proxy_to_app;
    }

    location / {
        return 301 https://$host$request_uri;
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
}