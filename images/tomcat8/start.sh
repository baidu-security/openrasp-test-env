#!/bin/bash

cp -R /test-application/java/webapps /usr/local/tomcat

/bin/bash /rasp-installers/install-rasp-java.sh

/bin/bash /etc/init.d/tomcat.sh start

nohup python /root/pyhttp/http.py &>/dev/null &

/bin/bash
