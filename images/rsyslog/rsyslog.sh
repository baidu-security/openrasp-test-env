#!/bin/bash

case "$1" in
    start)
        echo '[-] Starting rsyslogd'
        rsyslogd &>/root/rsyslogd.log   
    ;;
    stop)
        echo '[-] Stopping rsyslogd'
        killall rsyslogd
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
