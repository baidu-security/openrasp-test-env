#!/bin/bash

case "$1" in
    start)
        echo '[-] Starting php-fpm'
        php-fpm -D &>/root/php-fpm.log   
    ;;
    stop)
        echo '[-] Stopping php-fpm'
        killall php-fpm
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
