#!/bin/bash

tomcat_base=/usr/local/tomcat
chmod +x "$tomcat_base"/bin/*.sh

case "$1" in
    start)
		echo '[-] Starting Tomcat'
        bash "$tomcat_base"/bin/startup.sh

        echo '[-] Waiting for Tomcat to start'
		while true
		do
			curl -I 127.0.0.1:8080 2>/dev/null && break
			sleep 1
		done
    ;;
    stop)
		echo '[-] Stopping Tomcat'
        bash "$tomcat_base"/bin/shutdown.sh
		killall java
    ;;
    restart)
		$0 stop
		$0 start
	;;
    *)
		echo Unknown action: $1
	;;

esac
