#!/bin/bash

IP=`ping elasticsearch6.4.2 -c 1 | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'| head -n 1`
echo "$(sed -r "s/[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:9200/${IP}:9200/g" /etc/logstash/conf.d/cloud.conf)" > /etc/logstash/conf.d/cloud.conf

/bin/bash /rasp-installers/install-rasp-cloud.sh

/bin/bash /etc/init.d/logstash.sh start

/bin/bash /etc/init.d/rasp-cloud.sh start

/bin/bash
