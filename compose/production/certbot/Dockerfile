FROM certbot/certbot:latest

COPY ./compose/production/certbot/start.sh /opt/

RUN chmod +x /opt/start.sh

ENTRYPOINT []

CMD ["certbot", "renew"]

