#!/usr/bin/env python
# coding:utf-8

import socket
import sys
import json
import time

import envConfig
from serverAPI import cloudAPI, agentAPI


def check_res(res):
    if res is False:
        return False
    else:
        if res['status'] == 0:
            return True
        else:
            return False


def init_cloud_env():
    agent_api = agentAPI()
    cloud_api = cloudAPI()
    # 登录云控
    res_data = cloud_api.user_login(
        envConfig.rasp_account["username"], envConfig.rasp_account["password"])
    if res_data['status'] != 0:
        print("login fail!")
        exit()
    print("login cloud server!")
    # 打开用于生成配置的模板文件，模板本身已包含大部分配置
    with open("envConfig.py.origin", 'r') as f:
        env_content = f.read().decode('utf-8')
    for app in envConfig.app_info:
        app_id = ''
        secret = ''
        app_json = json.dumps(app['app_info'])
        res = cloud_api.api_app(app_json)
        if not check_res(res):
            print("app create error, check if exist!")
            res = cloud_api.api_app_get_page()
            if not check_res(res):
                print("app create fail!")
                exit()
            else:
                res_data = res['data']['data']
                for app_exist in res_data:
                    if app_exist['name'] == app['app_info']['name']:
                        app_id = app_exist['id']
                        secret = app_exist['secret']
        else:
            app_id = res['data']['id']
            secret = res['data']['secret']
        if app_id == '':
            print("app create fail!")
            exit()
        var = u'[[appid-' + app['app_info']['name'].decode('utf-8') + u']]'
        env_content = env_content.replace(var, app_id)
        # 上传noplugin插件
        res_data = cloud_api.api_plugin_upload(app_id, envConfig.plugin_info['noplugin']['path'])
        if res_data['status'] != 0:
            print("upload plugin fail!")
            exit()
        # 配置该APP下的agent
        for hostname in app["agents"]:
            if not agent_api.api_change_cloud_config(hostname, app_id, secret):
                print("change agent config fail!")
                exit()
    with open("envConfig.py", 'w') as f:
        f.write(env_content.encode('utf-8'))
    print("appid registed on cloud server, agent config changed")
    agent_api.restart_all()
    print("restarting agents , please wait...")
    # 测试agent是否成功连接
    online_servers = 0
    for i in range(1, 11):
        time.sleep(10)
        print("Checking if agent is online , times:" + str(i))
        res_data = cloud_api.api_rasp_search("{}", 1, 1000)
        if not check_res:
            print("search rasp agent fail!")
            exit()
        else:
            if (res_data['status'] != 0):
                print("unexpected json data from cloud!")
                print("server response:")
                print(res_data.text.encode("utf-8"))
                exit()
            else:
                online_servers = res_data['data']['total']
                if online_servers == len(envConfig.rasp_agents):
                    break
    if online_servers != len(envConfig.rasp_agents):
        print("init failed, some agent are not online!")
        exit()

if __name__ == "__main__":
    init_cloud_env()
    print("init success!")
