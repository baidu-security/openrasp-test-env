FROM debian:stretch-slim 

COPY logstash.sh /etc/init.d/logstash.sh
RUN chmod +x /etc/init.d/logstash.sh

COPY start.sh /root

RUN echo "deb http://http.debian.net/debian stretch main contrib non-free" > /etc/apt/sources.list.d/stretch.list
RUN apt-get update && apt-get install -y wget procps curl iputils-ping vim
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y --no-install-recommends openjdk-8-jre-headless
RUN wget --no-check-certificate https://artifacts.elastic.co/downloads/logstash/logstash-6.4.2.deb 
RUN dpkg -i logstash-6.4.2.deb  && rm logstash-6.4.2.deb

RUN rm /etc/logstash/logstash-sample.conf


ENTRYPOINT ["/bin/bash", "/root/start.sh"]
