######
# See: https://hub.docker.com/_/php/
######

FROM php:7.2-fpm
MAINTAINER lixin1234qqq <lixin1234qqq@gmail.com>

######
# You can install php extensions using docker-php-ext-install
######

RUN apt-get update && apt-get install -y \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng-dev
RUN docker-php-ext-install -j$(nproc) iconv mysqli pdo_mysql\
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd

RUN apt-get install -y procps python

COPY php-fpm.sh /etc/init.d/php-fpm.sh
RUN chmod +x /etc/init.d/php-fpm.sh
COPY start.sh /root
COPY restart.sh /root/pyhttpfile/restart.sh

ENTRYPOINT ["/bin/bash", "/root/start.sh"]