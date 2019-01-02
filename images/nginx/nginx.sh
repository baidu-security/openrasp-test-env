#!/bin/bash

case "$1" in
    start)
        echo '[-] Starting Nginx'
        nginx

        echo '[-] Waiting for Nginx to start'
        while true
        do
            curl -I 127.0.0.1:80 &>/dev/null && break
            sleep 1
        done
    ;;
    stop)
        echo '[-] Stopping Nginx'
        killall nginx
    ;;
    restart)
		$0 stop
        sleep 1
		$0 start
	;;
    *)
		echo Unknown action: $1
	;;

esac
