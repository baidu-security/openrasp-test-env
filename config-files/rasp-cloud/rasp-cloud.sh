#!/bin/sh

case "$1" in
    start)
        echo '[-] Starting rasp-cloud'
        echo '[-] Waiting for Mongodb to start'
        while true
        do
            curl mongodb3.6:27017 &>/dev/null && break
            sleep 1
        done
        echo '[-] Waiting for elasticsearch to start'
        while true
        do
            curl -I elasticsearch6.4.2:9200 &>/dev/null && break
            sleep 1
        done
        bash -c "nohup /rasp-cloud-panel/rasp-cloud -type=panel &>/rasp-cloud-panel/cloud-panel-nohup.log &"
        sleep 10
        bash -c "nohup /rasp-cloud-agent/rasp-cloud -type=agent &>/rasp-cloud-agent/cloud-agent-nohup.log &"
        echo '[-] rasp-cloud start success'
    ;;
    stop)
        echo '[-] Stopping rasp-cloud'
        killall rasp-cloud
    ;;
    restart)
        $0 stop
        $0 start
    ;;
    *)
        echo Unknown action: $1
    ;;

esac