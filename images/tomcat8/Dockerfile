FROM tomcat:8.5.34-jre8

COPY tomcat.sh /etc/init.d/tomcat.sh
RUN chmod +x /etc/init.d/tomcat.sh

COPY start.sh /root

COPY restart.sh /root/pyhttpfile/restart.sh

RUN apt-get update && apt-get -y install procps python

ENTRYPOINT ["/bin/bash", "/root/start.sh"]