FROM php:5.6-apache

COPY start.sh /root

COPY restart.sh /root/pyhttpfile/restart.sh

RUN apt-get update
RUN apt-get install -y python


ENTRYPOINT ["/bin/bash", "/root/start.sh"]
EXPOSE 80