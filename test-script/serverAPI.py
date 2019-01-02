#!/usr/bin/env python
# coding:utf-8

import requests
import json
import time
import random
import string

import envConfig
import dockerDNS


class agentAPI(object):

    def __init__(self):
        self.agents = envConfig.rasp_agents

    # http code 为200时，返回接口json，否则返回False
    def check_res(self, url, res):
        if res.status_code == 200:
            return True
        else:
            text = res.text
            try:
                error_msg = "[agentAPI] api {url} return error: {error}".format(
                    url=url, error=json.loads(text, encoding="utf-8")["status"].encode("utf-8"))
            except:
                error_msg = "[agentAPI] api {url} return unexpected content".format(
                    url=url)
            print(error_msg)
            return False

    # 重启接口
    def api_restart(self, hostname):
        url = "http://" + hostname + ":" + \
            self.agents[hostname]['pyport'] + "/restart"
        data = "{}"
        res = requests.post(url=url, data=data)
        return self.check_res(url, res)

    # 云控配置接口
    def api_change_cloud_config(self, hostname, appid, secret):
        url = "http://" + hostname + ":" + \
            self.agents[hostname]['pyport'] + "/change_cloud_config"
        data = '''{{
            "rasp_type":"{}",
            "app_id":"{}",
            "secret":"{}"
        }}'''.format(self.agents[hostname]['type'], appid, secret)
        res = requests.post(url=url, data=data)
        return self.check_res(url, res)

    # 重启所有服务
    def restart_all(self):
        for agent in self.agents:
            res = self.api_restart(agent)
            if not res:
                print("[agentAPI] restart all server failed!")
                return False
        return True


class cloudAPI(object):

    # cloud_addr: http://raps-cloud:8080
    def __init__(self):
        self.cloud_addr = envConfig.rasp_cloud_url
        self.s = requests.Session()

    def check_res(self, res, api_name):
        if res.status_code != 200:
            raise Exception("[cloudAPI] api function {} retured http code {}".format(api_name, res.status_code))
        else:
            try:
                res_data = json.loads(res.text, encoding="utf-8")
            except:
                raise Exception("[cloudAPI] api function {} response json decode error".format(api_name))
            # 返回json decode后的数据
            return res_data

    

    # 登录登出接口

    # 登录接口
    def user_login(self, username, password):
        url = self.cloud_addr + "/v1/user/login"
        data = """
        {{
            "username":"{}",
            "password":"{}"
        }}
        """.format(username, password)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "user_login")

    # 登出接口
    def user_logout(self):
        url = self.cloud_addr + "/v1/user/logout"
        res = self.s.get(url=url)
        return self.check_res(res, "user_logout")

    # 获取是否登录
    def user_islogin(self):
        url = self.cloud_addr + "/v1/user/islogin"
        data = """
        {{
        }}
        """.format()
        res = self.s.post(url=url, data=data)
        return False if res.status_code == 401 else True

    # 更改密码接口
    def user_update(self, old_password, new_password):
        url = self.cloud_addr + "/v1/user/update"
        data = """
        {{
            "old_password":"{}",
            "new_password":"{}"
        }}
        """.format(old_password, new_password)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "user_update")

    # 插件管理接口
    # 上传插件
    def api_plugin_upload(self, app_id, plugin_file_path):
        url = self.cloud_addr + "/v1/api/plugin?app_id=" + app_id
        files = {'plugin': open(plugin_file_path, 'rb')}
        res = self.s.post(url=url, files=files)
        return self.check_res(res, "api_plugin_upload")

    # 获取插件
    def api_plugin_get(self, app_id, page=1, perpage=1000):
        url = self.cloud_addr + "/v1/api/plugin/get"
        data = """
        {{
            "app_id":"{}",
            "page":{},
            "perpage":{}
        }}
        """.format(app_id, page, perpage)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_plugin_get")

    # 删除插件
    def api_plugin_delete(self, plugin_id):
        url = self.cloud_addr + "/v1/api/plugin/delete"
        data = """
        {{
            "id":"{}"
        }}
        """.format(plugin_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_plugin_delete")

    # App管理接口

    # 添加/修改 一个 APP
    def api_app(self, api_json_data):
        url = self.cloud_addr + "/v1/api/app"
        res = self.s.post(url=url, data=api_json_data)
        return self.check_res(res, "api_json_data")

    # 删除一个 APP
    def api_app_delete(self, app_id):
        url = self.cloud_addr + "/v1/api/app/delete"
        data = """
        {{
            "id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_delete")

    # 获取 App
    def api_app_get(self, app_id):
        url = self.cloud_addr + "/v1/api/app/get"
        data = """
        {{
            "app_id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_get")

    # 下发通用配置
    def api_app_general_config(self, app_id, config_json):
        url = self.cloud_addr + "/v1/api/app/general/config"
        data = """
        {{
            "app_id":"{}",
            "config":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_general_config")

    # 下发算法配置
    def api_plugin_algorithm_config(self, plugin_id, config_json):
        url = self.cloud_addr + "/v1/api/plugin/algorithm/config"
        data = """
        {{
            "id":"{}",
            "config":{}
        }}
        """.format(plugin_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_plugin_algorithm_config")

    # 下发白名单配置
    def api_app_whitelist_config(self, app_id, config_json):
        url = self.cloud_addr + "/v1/api/app/whitelist/config"
        data = """
        {{
            "app_id":"{}",
            "config":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_whitelist_config")

    # 恢复默认配置
    def api_plugin_algorithm_restore(self, app_id, config_json):
        url = self.cloud_addr + "v1/api/plugin/algorithm/restore"
        data = """
        {{
            "app_id":"{}",
            "config":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_plugin_algorithm_restore")

    # 下发email报警配置
    def api_app_alarm_config_email(self, app_id, config_json):
        url = self.cloud_addr + "/v1/api/app/alarm/config"
        data = """
        {{
            "app_id":"{}",
            "email_alarm_conf":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_alarm_config_email")

    # 下发钉钉报警配置
    def api_app_alarm_config_ding(self, app_id, config_json):
        url = self.cloud_addr + "/v1/api/app/alarm/config"
        data = """
        {{
            "app_id":"{}",
            "ding_alarm_conf":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_alarm_config_ding")

    # 下发http报警配置
    def api_app_alarm_config_http(self, app_id, config_json):
        url = self.cloud_addr + "/v1/api/app/alarm/config"
        data = """
        {{
            "app_id":"{}",
            "http_alarm_conf":{}
        }}
        """.format(app_id, config_json)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_alarm_config_http")

    # 获取 APP 下所有 RASP
    def api_app_rasp_get(self, app_id, page=1, perpage=1000):
        url = self.cloud_addr + "/v1/api/app/rasp/get"
        data = """
        {{
            "app_id":"{}",
            "page":{},
            "perpage":{}
        }}
        """.format(app_id, page, perpage)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_rasp_get")

    # 获取 APP 下的所有插件
    def api_app_plugin_get(self, app_id, page=1, perpage=1000):
        url = self.cloud_addr + "/v1/api/app/plugin/get"
        data = """
        {{
            "app_id":"{}",
            "page":{},
            "perpage":{}
        }}
        """.format(app_id, page, perpage)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_plugin_get")

    # 获取 APP 下选中的插件
    def api_app_plugin_select_get(self, app_id):
        url = self.cloud_addr + "/v1/api/app/plugin/select/get"
        data = """
        {{
            "app_id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_plugin_select_get")

    # 设置 APP 下选中的插件
    def api_app_plugin_select(self, app_id, plugin_id):
        url = self.cloud_addr + "/v1/api/app/plugin/select"
        data = """
        {{
            "app_id":"{}",
            "plugin_id":"{}"
        }}
        """.format(app_id, plugin_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_plugin_select")

    # 测试邮件报警
    def api_app_email_test(self, app_id):
        url = self.cloud_addr + "/v1/api/app/email/test"
        data = """
        {{
            "app_id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_email_test")

    # 测试钉钉报警
    def api_app_ding_test(self, app_id):
        url = self.cloud_addr + "/v1/api/app/ding/test"
        data = """
        {{
            "app_id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_ding_test")

    # 测试 HTTP 报警
    def api_app_http_test(self, app_id):
        url = self.cloud_addr + "/v1/api/app/http/test"
        data = """
        {{
            "app_id":"{}"
        }}
        """.format(app_id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_app_http_test")

    # RASP管理接口

    # 按条件获取 RASP
    def api_rasp_search(self, search_data, page=1, perpage=1000):
        url = self.cloud_addr + "/v1/api/rasp/search"
        data = """
        {{
            "page":{},
            "perpage":{},
            "data":{}
        }}
        """.format(page, perpage, search_data)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_rasp_search")

    # 删除一个 RASP
    def api_rasp_delete(self, id):
        url = self.cloud_addr + "/v1/api/rasp/delete"
        data = """
        {{
            "id":"{}"
        }}
        """.format(id)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_rasp_delete")

    # 静态Token管理接口

    # 生成新的 token
    def api_token(self, description):
        url = self.cloud_addr + "/v1/api/token"
        data = """
        {{
            "description":"{}"
        }}
        """.format(description)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_token")

    # 获取所有 token
    def api_token_get(self, page=1, perpage=1000):
        url = self.cloud_addr + "/v1/api/token"
        data = """
        {{
            "page":{},
            "perpage":{}
        }}
        """.format(page, perpage)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_token_get")
    
    # token 访问测试
    def api_token_get_with_token(self, token):
        url = self.cloud_addr + "/v1/api/token/get"
        data = """{
            "page":1,
            "perpage":1000
        }"""
        headers = {"X-OpenRASP-Token": token}
        res = requests.post(url=url, data=data, headers=headers)
        return self.check_res(res, "api_token_get_use_token")

    # 删除token
    def api_token_delete(self, token):
        url = self.cloud_addr + "/v1/api/token/delete"
        data = """
        {{
            "token":"{}"
        }}
        """.format(token)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_token_delete")

    # 请求统计接口

    # 请求统计信息聚合
    def api_report_dashboard(self, app_id, start_time="0", end_time="4100688000", interval="hour", time_zone="+08:00"):
        url = self.cloud_addr + "/v1/api/report/dashboard"
        data = """
        {{
            "app_id":"{}",
            "start_time":"{}",
            "end_time":"{}",
            "interval":"{}",
            "time_zone":"{}"
        }}
        """.format(app_id, start_time, end_time, interval, time_zone)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_report_dashboard")

    # 报警接口

    # 按照时间聚合攻击日志
    def api_log_attack_aggr_time(self, app_id, start_time="0", end_time="4100688000", interval="hour", time_zone="+08:00"):
        url = self.cloud_addr + "/v1/api/log/attack/aggr/time"
        data = """
        {{
            "app_id":"{}",
            "start_time":"{}",
            "end_time":"{}",
            "interval":"{}",
            "time_zone":"{}"
        }}
        """.format(app_id, start_time, end_time, interval, time_zone)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_log_attack_aggr_time")

    # 按照类型聚合攻击日志
    def api_log_attack_aggr_type(self, app_id, start_time="0", end_time="4100688000", size=10):
        url = self.cloud_addr + "/v1/api/log/attack/aggr/type"
        data = """
        {{
            "app_id":"{}",
            "start_time":"{}",
            "end_time":"{}",
            "size":"{}"
        }}
        """.format(app_id, start_time, end_time, size)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_log_attack_aggr_type")

    # 按照 UA 聚合攻击日志
    def api_log_attack_aggr_ua(self, app_id, start_time="0", end_time="4100688000", size=10):
        url = self.cloud_addr + "/v1/api/log/attack/aggr/ua"
        data = """
        {{
            "app_id":"{}",
            "start_time":"{}",
            "end_time":"{}",
            "size":"{}"
        }}
        """.format(app_id, start_time, end_time, size)
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_log_attack_aggr_ua")

    # 攻击报警搜索 / csv导出
    def api_log_attack_search(self, data):
        url = self.cloud_addr + "/v1/api/log/attack/search"
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_log_attack_search")

    # 基线报警搜索 / csv导出
    def api_log_policy_search(self, data):
        url = self.cloud_addr + "/v1/api/log/policy/search"
        res = self.s.post(url=url, data=data)
        return self.check_res(res, "api_log_policy_search")


class webappAPI(object):

    def __init__(self):
        for hostname in envConfig.rasp_agents:
            front_name = envConfig.rasp_agents[hostname]['webfront']
            ip = dockerDNS.getAddr(front_name)
            envConfig.rasp_agents[hostname]['front_ip'] = ip
        self.agents = envConfig.rasp_agents

    def is_rasp_running(self, hostname):
        info = self.agents[hostname]
        url = "http://" + info['front_ip'] + ":" + info['port'] + info['test-path']
        res = requests.get(url=url)
        if 'X-Protected-By' in res.headers:
            return True
        else:
            return False

    def test_block(self, hostname, path, user_agent):
        info = self.agents[hostname]
        url = "http://" + info['front_ip'] + ":" + info['port'] + path
        headers = {"User-Agent": user_agent}
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        if res.status_code == 302:
            return True
        else:
            return False


class testAPI(object):
    def __init__(self):
        self.cloud_api = cloudAPI()
        self.agent_api = agentAPI()
        self.webapp_api = webappAPI()
        # 初始化，登录云控
        login_res_data = self.cloud_api.user_login(
            envConfig.rasp_account["username"], envConfig.rasp_account["password"])
        if login_res_data is False or (login_res_data['status'] != 0):
            raise Exception("test init error: login failed!")

    def _get_random_str(self, length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    # 判断某app是否存在某版本插件
    def has_plugin(self, app_id, version):
        res_data = self.cloud_api.api_plugin_get(app_id)
        if res_data is False or res_data['status'] != 0:
            raise Exception("[testAPI] get plugin list failed!")
        for data in res_data['data']:
            if data['version'] == version:
                return True
        return False

    def delete_plugin(self, plugin_id):
        res_data = self.cloud_api.api_plugin_delete(plugin_id)
        if res_data['status'] != 0:
            return False
        return True

    def upload_plugin(self, app_id, path):
        res_data = self.cloud_api.api_plugin_upload(app_id, path)
        if res_data['status'] != 0:
            return False
        return True

    def get_app_plugin_list(self, app_id):
        res_data = self.cloud_api.api_app_plugin_get(app_id)
        if res_data['status'] != 0:
            return False
        return res_data['data']['data']

    def get_app_selected_plugin_list(self, app_id):
        res_data = self.cloud_api.api_app_plugin_select_get(app_id)
        if res_data['status'] != 0:
            return False
        return res_data['data']['data']

    def select_plugin(self, app_id, plugin_id):
        res_data = self.cloud_api.api_app_plugin_select(app_id, plugin_id)
        if res_data['status'] != 0:
            return False
        return True

    def search_rasp(self, data):
        res_data = self.cloud_api.api_rasp_search(data)
        if res_data['status'] != 0:
            return False
        return res_data['data']['data']

    def delete_rasp(self, rasp_id):
        res_data = self.cloud_api.api_rasp_delete(rasp_id)
        if res_data['status'] != 0:
            return False
        return True

    def get_attack_log_by_appid(self, appid):
        data = '''{{
            "data":{{
                "appid":"{}",
                "start_time":1522000000000,
                "end_time":1643000000000
            }},
            "page":1,
            "perpage":10
        }}'''.format(appid)
        res_data = self.cloud_api.api_log_attack_search(data)
        if res_data['status'] != 0:
            return False
        return res_data['data']['data']

    def test_block_request(self, hostname, test_path):
        user_agent = self._get_random_str(32)
        if self.webapp_api.test_block(hostname, test_path, user_agent) is False:
            return False
        else:
            return user_agent

    def restart_agent(self, hostname):
        self.agent_api.api_restart(hostname)
        for i in range(10):
            time.sleep(5)
            try:
                if self.webapp_api.is_rasp_running(hostname):
                    return True
            except:
                pass
        return False

    def set_white_list_all(self, appid, url):
        data = '''[{{
            "url":"{}",
            "hook":{{
                "all":true
            }}
        }}]'''.format(url)
        res_data = self.cloud_api.api_app_whitelist_config(appid, data)
        if res_data['status'] != 0:
            return False
        return True

    def set_white_list_none(self, appid):
        data = '[]'
        res_data = self.cloud_api.api_app_whitelist_config(appid, data)
        if res_data['status'] != 0:
            return False
        return True

    def edit_algorithm_config(self, app_id, plugin_id, config_key, config_value):
        res_data = self.cloud_api.api_app_plugin_get(app_id)
        if res_data['status'] != 0:
            return False
        algorithm_config = False
        for plugin in res_data['data']['data']:
            if plugin['id'] == plugin_id:
                algorithm_config = plugin['algorithm_config']
                break
        if algorithm_config is False or config_key not in algorithm_config:
            return False
        algorithm_config[config_key]["action"] = config_value
        res_data = self.cloud_api.api_plugin_algorithm_config(plugin_id, json.dumps(algorithm_config))
        if res_data['status'] != 0:
            return False
        return True

    def add_random_app(self):
        api_data = {
            "name": "test-app-" + self._get_random_str(16),
            "language":"java",
            "description": "test-description-" + self._get_random_str(16)
        }
        json_api_data = json.dumps(api_data)
        res_data = self.cloud_api.api_app(json_api_data)
        app_id = res_data['data']['id']
        res_data = self.cloud_api.api_app_get(app_id)
        if len(res_data['data']) > 0:
            return app_id
        else:
            return None

    def change_app_general_config(self, app_id):
        config = {
            "block.content_html": "ffff",
            "block.content_json": "qwe",
            "block.content_xml": "asd",
            "block.redirect_url": "xyz",
            "block.status_code": 403,
            "body.maxbytes": 8192,
            "clientip.header": "ClientIPS",
            "log.maxstack": 33,
            "ognl.expression.minlength": 44,
            "plugin.filter": True,
            "plugin.maxstack": 111,
            "plugin.timeout.millis": 112,
            "syslog.tag":    "RASSP",
            "syslog.url":     "url",
            "syslog.facility":  12,
            "syslog.enable":  False
        }
        config_json = json.dumps(config)
        self.cloud_api.api_app_general_config(app_id, config_json)
        res_data = self.cloud_api.api_app_get(app_id)
        res = res_data["data"]["general_config"]
        for item in config:
            if config[item] != res[item]:
                return False
        return True

    def del_app(self, app_id):
        self.cloud_api.api_app_delete(app_id)
        res_data = self.cloud_api.api_app_get(app_id)
        if res_data['status'] == 400:
            return True
        else:
            return False

    def get_new_token(self):
        res_data = self.cloud_api.api_token("test")
        token = res_data["data"]["token"]
        return token

    def test_token(self, token):
        res_data = self.cloud_api.api_token_get_with_token(token)
        if res_data["status"] == 0:
            return True
        else:
            return False

    def del_token(self, token):
        res_data = self.cloud_api.api_token_delete(token)
        if res_data["status"] != 0:
            return False
        else:
            return True