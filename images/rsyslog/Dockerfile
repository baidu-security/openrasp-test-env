FROM debian:stretch-slim 

RUN apt-get update && apt-get install -y rsyslog

COPY rsyslog.sh /etc/init.d/rsyslog.sh
RUN chmod +x /etc/init.d/rsyslog.sh

COPY start.sh /root

ENTRYPOINT ["/bin/bash", "/root/start.sh"]