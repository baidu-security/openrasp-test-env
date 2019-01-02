# coding=utf-8

import BaseHTTPServer
import struct
import fcntl
import os
import urllib
import os
import re
import json


class ServerHTTP(BaseHTTPServer.BaseHTTPRequestHandler):

    actions = ["restart", "change_cloud_config"]

    def restart(self, args):
        os.system("bash /root/pyhttpfile/restart.sh")
    ''' 
        参数示例：
        {
            "rasp_type":"java",
            "app_id":"xxxxx"
        }
    '''

    def change_cloud_config(self, args):
        rasp_type = args['rasp_type']
        app_id = args['app_id'].encode('utf-8')
        secret = args['secret'].encode('utf-8')
        cloud_serv_url = "http://rasp-cloud:8087"
        if rasp_type == "java":
            config_path = "/usr/local/tomcat/rasp/conf/rasp.properties"
            with open(config_path, 'r') as f:
                content = f.read()
            content = re.sub(r'[# ]*cloud\.enable\s*=\s*.*',
                             'cloud.enable=true', content, flags=re.IGNORECASE)
            content = re.sub(r'[# ]*cloud\.backend_url\s*=\s*.*',
                             'cloud.backend_url=' + cloud_serv_url, content, flags=re.IGNORECASE)
            content = re.sub(r'[# ]*cloud\.app_id\s*=\s*.*',
                             'cloud.app_id=' + app_id, content, flags=re.IGNORECASE)
            content = re.sub(r'[# ]*cloud\.app_secret\s*=\s*.*',
                             'cloud.app_secret=' + secret, content, flags=re.IGNORECASE)
            content = re.sub(r'[# ]*cloud\.heartbeat_interval\s*=\s*.*',
                             'cloud.heartbeat_interval=10', content, flags=re.IGNORECASE)
            with open(config_path, 'w') as f:
                f.write(content)
        elif rasp_type == "php":
            config_path = "/usr/local/etc/php/conf.d/z_openrasp.ini"
            if not os.path.isfile(config_path):
                config_path = "/usr/local/etc/php/php.ini"
            with open(config_path, 'r') as f:
                content = f.read()
            content = re.sub(r'[; ]*openrasp\.remote_management_enable\s*=\s*.*',
                             'openrasp.remote_management_enable=1', content, flags=re.IGNORECASE)
            content = re.sub(r'[; ]*openrasp\.backend_url\s*=\s*.*',
                             'openrasp.backend_url=' + cloud_serv_url, content, flags=re.IGNORECASE)
            content = re.sub(r'[; ]*openrasp\.app_id\s*=\s*.*',
                             'openrasp.app_id=' + app_id, content, flags=re.IGNORECASE)
            content = re.sub(r'[; ]*openrasp\.app_secret\s*=\s*.*',
                             'openrasp.app_secret=' + secret, content, flags=re.IGNORECASE)
            content = re.sub(r'[; ]*openrasp\.heartbeat_interval\s*=\s*.*',
                             'openrasp.heartbeat_interval=10', content, flags=re.IGNORECASE)

            with open(config_path, 'w') as f:
                f.write(content)
        else:
            raise Exception("rasp type error")

    def do_GET(self):
        self.send_response(403)
        buf = '''{
            "status":"method not allow"
        }
        '''
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(buf)

    def do_POST(self):
        path = self.path
        query = urllib.splitquery(path)
        action = query[0][1:]
        datas = self.rfile.read(int(self.headers['content-length']))
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        try:
            args = json.loads(datas)
            buf = ""
            if action in self.actions:
                func = getattr(self, action)
                func(args)
                self.send_response(200)
                buf = '''{
                    "status":"ok"
                }
                '''
            else:
                self.send_response(404)
                buf = '''{
                    "status":"action not found"
                }
                '''
        except Exception as e:
            self.send_response(500)
            buf = '''{{
                "status":"{}"
            }}
            '''
            buf = buf.format(e)

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(buf)


class WebServer(BaseHTTPServer.HTTPServer):
    def __init__(self, *args, **kwargs):
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)
        # Set FD_CLOEXEC flag
        flags = fcntl.fcntl(self.socket.fileno(), fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(self.socket.fileno(), fcntl.F_SETFD, flags)


def start_server(port):
    http_server = WebServer(('', int(port)), ServerHTTP)
    http_server.serve_forever()


if __name__ == "__main__":
    start_server(16789)
