#!/usr/bin/env python
# coding:utf-8

rasp_agents = {
    "tomcat8": {
        "port": "8080",
        "pyport": "16789",
        "type": "java",
        "webfront": "tomcat8",
        "front_ip": "",
        "test-path": "/index.jsp",
        "test-dir-path": "/vulns/001-dir-1.jsp?dirname=../../../../../../../var/log/",
        "test-cmd-path": "/vulns/004-command-2.jsp?cmd=ls -la /",
        "test-ssrf-path": "/vulns/011-ssrf-commons-httpclient.jsp?url=http://0x7f001",
        "appid": "4b46cdeb3e5b7ab5b11754681b054ae5e8f9785b"
    },
    "apache-php5.6": {
        "port": "80",
        "pyport": "16789",
        "type": "php",
        "webfront": "apache-php5.6",
        "front_ip": "",
        "test-path": "/index.php",
        "test-dir-path": "/vulns/001-dir.php?dir=/proc",
        "test-ssrf-path": "/vulns/011-ssrf-curl.php?url=http://0x7f001",
        "appid": "a46057306d0de81c3856a9f62e9ce7b2384e1446"
    },
    "apache-php7.2": {
        "port": "80",
        "pyport": "16789",
        "type": "php",
        "webfront": "apache-php7.2",
        "front_ip": "",
        "test-path": "/index.php",
        "test-dir-path": "/vulns/001-dir.php?dir=/proc",
        "test-ssrf-path": "/vulns/011-ssrf-curl.php?url=http://0x7f001",
        "appid": "a46057306d0de81c3856a9f62e9ce7b2384e1446"
    },
    "php5.6-fpm": {
        "port": "80",
        "pyport": "16789",
        "type": "php",
        "webfront": "nginx-php5.6",
        "front_ip": "",
        "test-path": "/index.php",
        "test-dir-path": "/vulns/001-dir.php?dir=/proc",
        "test-ssrf-path": "/vulns/011-ssrf-curl.php?url=http://0x7f001",
        "appid": "bf5f56f3986439716e367dd168a323f29e5df643"
    },
    "php7.2-fpm": {
        "port": "80",
        "pyport": "16789",
        "type": "php",
        "webfront": "nginx-php7.2",
        "front_ip": "",
        "test-path": "/index.php",
        "test-dir-path": "/vulns/001-dir.php?dir=/proc",
        "test-ssrf-path": "/vulns/011-ssrf-curl.php?url=http://0x7f001",
        "appid": "bf5f56f3986439716e367dd168a323f29e5df643",
    }
}

app_info = [
    {
        "app_info": {
            "id": "4b46cdeb3e5b7ab5b11754681b054ae5e8f9785b",
            "name": "tomcat-java-test",
            "language": "java",
            "description": "openrasp tomcat-java"
        },
        # 使用此信息的agent主机名
        "agents": ["tomcat8"]
    },
    {
        "app_info": {
            "id": "bf5f56f3986439716e367dd168a323f29e5df643",
            "name": "php-fpm-test",
            "language": "php",
            "description": "openrasp php-fpm"
        },
        # 使用此信息的agent主机名
        "agents": ["php5.6-fpm", "php7.2-fpm"]
    },
    {
        "app_info": {
            "id": "a46057306d0de81c3856a9f62e9ce7b2384e1446",
            "name": "apache-php-test",
            "language": "php",
            "description": "openrasp apache-php"
        },
        # 使用此信息的agent
        "agents": ["apache-php5.6", "apache-php7.2"]
    }
]

syslog_name = "rsyslog"
rasp_cloud_url = "http://rasp-cloud:8080"
rasp_cloud_serv_url = "http://rasp-cloud:8087"
rasp_account = {
    "username": "openrasp",
    "password": "admin@123",
    "default_password": "admin@123",
}

plugin_info = {
    "official_1": {
        "path": "plugin/official.js",
        "version": "2018-1119-2100"
    },
    "noplugin": {
        "path": "plugin/noplugin.js",
        "version": "2018-1025-0001"
    },
}
