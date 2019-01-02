#!/bin/bash
cp -R /rasp-installers/rasp-cloud /rasp-cloud-agent
cp -R /rasp-installers/rasp-cloud /rasp-cloud-panel

cp /rasp-cloud-config/rasp-cloud-agent/app.conf /rasp-cloud-agent/conf/app.conf 
cp /rasp-cloud-config/rasp-cloud-panel/app.conf /rasp-cloud-panel/conf/app.conf 

cp /rasp-cloud-config/rasp-cloud.sh /etc/init.d/rasp-cloud.sh
chmod +x /etc/init.d/rasp-cloud.sh
