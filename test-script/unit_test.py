#!/usr/bin/env python
# coding:utf-8

import unittest
import json
import time

import envConfig

from serverAPI import cloudAPI, agentAPI, webappAPI, testAPI

import requests


class testAll(unittest.TestCase):

    def __init__(self):
        self.log_delay_time = 20
        self.heartbeat_time = 20

    def test_example(self):
        self.assertTrue(1)
        self.assertEquals(1, 2)

    # 测试插件上传、选中、删除的过程
    def test_1(self, app_hostname):
        test_api = testAPI()
        plugin_info = envConfig.plugin_info['official_1']
        noplugin_info = envConfig.plugin_info['noplugin']
        agent_info = envConfig.rasp_agents[app_hostname]

        # step 1 上传
        print("[test] Upload plugin, version: {}".format(plugin_info['version']))
        if test_api.upload_plugin(agent_info['appid'], plugin_info['path']) is False:
            print("[test] Fail in step 1")
            return False
        # 上传空插件
        print("[test] Upload noplugin, version: {}".format(noplugin_info['version']))
        if test_api.upload_plugin(agent_info['appid'], noplugin_info['path']) is False:
            print("[test] Fail in step 1")
            return False

        # step 2 获取
        plugin_list = test_api.get_app_plugin_list(agent_info['appid'])
        if plugin_list is False:
            print("[test] Fail in step 2")
            return False
        
        # step 3 选中
        plugin_id = ""
        for plugin in plugin_list:
            if plugin['version'] == plugin_info['version']:
                plugin_id = plugin['id']
                break
        if plugin_id == "":
            print("[test] Fail in step 3")
            return False
        test_api.select_plugin(agent_info['appid'], plugin_id)

        # step 4 等待下发
        print("[test] wait for plugin apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 5 测试vuln
        print("[test] testing if plugin has been applied")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is False:
            print("[test] Fail in step 5")
            return False

        # step 6 获取vuln日志
        print("[test] wait for agent log upload to cloud, sleep 1 log delay cycle")
        time.sleep(self.log_delay_time)
        log_list = test_api.get_attack_log_by_appid(user_agent)
        found_times = 0
        if log_list is False:
            print("[test] Fail in step 6")
            return False
        for attack_log in log_list:
            if attack_log['user_agent'] == user_agent:
                found_times += 1
                break
        if found_times > 1 or found_times == 0:
            print("[test] Fail in step 6 , found {} log in 1 attack".format(str(found_times)))
            return False

        # step 7 重启服务
        print("[test] testing restart service")
        if test_api.restart_agent(app_hostname) is False:
            print("[test] Fail in step 7")
            return False

        # step 8 再次测试vuln
        print("[test] testing if plugin still work after restart")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is False:
            print("[test] Fail in step 8")
            return False

        # step 9 再次获取vuln日志
        print("[test] wait for agent log upload to cloud, sleep 1 log delay cycle")
        time.sleep(self.log_delay_time)
        log_list = test_api.get_attack_log_by_appid(user_agent)
        found_times = 0
        if log_list is False:
            print("[test] Fail in step 9")
            return False
        for attack_log in log_list:
            if attack_log['user_agent'] == user_agent:
                found_times += 1
                break
        if found_times > 1 or found_times == 0:
            print("[test] Fail in step 9 , found {} log in 1 attack".format(str(found_times)))
            return False

        # step 10 测试删除使用中的插件
        print("[test] testing delete plugin in use")
        if test_api.delete_plugin(plugin_id) is True:
            print("[test] Fail in step 10")
            return False

        # step 11 选中noplugin
        noplugin_id = ""
        for plugin in plugin_list:
            if plugin['version'] == noplugin_info['version']:
                noplugin_id = plugin['id']
                break
        if noplugin_id == "":
            print("[test] Fail in step 11")
            return False
        print("[test] testing select noplugin")
        test_api.select_plugin(agent_info['appid'], noplugin_id)

        # step 12 测试删除未使用的插件
        print("[test] testing delete plugin not in use")
        for plugin in plugin_list:
            if plugin['id'] != noplugin_id:
                print("[test] try to delete plugin {}".format(plugin['id']))
                if test_api.delete_plugin(plugin['id']) is False:
                    print("[test] Fail in step 12")
                    return False

        # step 13 等待下发
        print("[test] wait for plugin apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 14 测试插件是否失效
        print("[test] testing if plugin has been overwritten")
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is not False:
            print("[test] Fail in step 14")
            return False

        return True

    # 测试配置开关、白名单
    def test_2(self, app_hostname):
        test_api = testAPI()
        plugin_info = envConfig.plugin_info['official_1']
        noplugin_info = envConfig.plugin_info['noplugin']
        agent_info = envConfig.rasp_agents[app_hostname]

        # step 1 上传
        print("[test] Upload plugin, version: {}".format(plugin_info['version']))
        if test_api.upload_plugin(agent_info['appid'], plugin_info['path']) is False:
            print("[test] Fail in step 1")
            return False

        # step 2 获取
        plugin_list = test_api.get_app_plugin_list(agent_info['appid'])
        if plugin_list is False:
            print("[test] Fail in step 2")
            return False

        # step 3 选中
        plugin_id = ""
        for plugin in plugin_list:
            if plugin['version'] == plugin_info['version']:
                plugin_id = plugin['id']
                break
        if plugin_id == "":
            print("[test] Fail in step 3")
            return False
        test_api.select_plugin(agent_info['appid'], plugin_id)

        # step 4 等待下发
        print("[test] wait for plugin apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 5 测试vuln
        print("[test] testing if plugin has been applied")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is False:
            print("[test] Fail in step 5")
            return False

        # step 6 获取vuln日志
        print("[test] wait for agent log upload to cloud, sleep 1 heartbeat cycle")
        time.sleep(self.log_delay_time)
        log_list = test_api.get_attack_log_by_appid(user_agent)
        found_times = 0
        if log_list is False:
            print("[test] Fail in step 6")
            return False
        for attack_log in log_list:
            if attack_log['user_agent'] == user_agent:
                found_times += 1
                break
        if found_times > 1 or found_times == 0:
            print("[test] Fail in step 6 , found {} log in 1 attack".format(str(found_times)))
            return False

        # step 7 配置全站白名单
        print("[test] configuring whitelist for all hook")
        if agent_info['port'] == "80":
            port = ""
        else:
            port = ":" + agent_info['port']
        if test_api.set_white_list_all(agent_info['appid'], agent_info['front_ip'] + port + "/vulns/") is False:
            print("[test] Fail in step 7")
        print("[test] wait for whitelist apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 8 测试白名单效果
        print("[test] testing if whitlist has been applied")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is not False:
            print("[test] Fail in step 8")
            return False

        # step 9 关闭全站白名单
        print("[test] remove whitelist for all")
        if test_api.set_white_list_none(agent_info['appid']) is False:
            print("[test] Fail in step 9")
        print("[test] wait for whitelist apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 10 测试关闭是否生效
        print("[test] testing if whitlist has been applied")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is False:
            print("[test] Fail in step 10")
            return False

        return True

    # 测试配置下发
    def test_3(self, app_hostname):
        test_api = testAPI()
        plugin_info = envConfig.plugin_info['official_1']
        noplugin_info = envConfig.plugin_info['noplugin']
        agent_info = envConfig.rasp_agents[app_hostname]

        # step 1 上传
        print("[test] Upload plugin, version: {}".format(plugin_info['version']))
        if test_api.upload_plugin(agent_info['appid'], plugin_info['path']) is False:
            print("[test] Fail in step 1")
            return False

        # step 2 获取
        plugin_list = test_api.get_app_plugin_list(agent_info['appid'])
        if plugin_list is False:
            print("[test] Fail in step 2")
            return False

        # step 3 选中
        plugin_id = ""
        for plugin in plugin_list:
            if plugin['version'] == plugin_info['version']:
                plugin_id = plugin['id']
                break
        if plugin_id == "":
            print("[test] Fail in step 3")
            return False
        test_api.select_plugin(agent_info['appid'], plugin_id)

        # step 4 等待下发
        print("[test] wait for plugin apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 5 测试vuln
        print("[test] testing if plugin has been applied")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is False:
            print("[test] Fail in step 5")
            return False

        # step 6 修改算法开关
        print("[test] edit algorithm config, switch off hook")
        if not test_api.edit_algorithm_config(agent_info['appid'], plugin_id, "directory_unwanted", "ignore"):
            print("[test] Fail in step 6")
            return False
        if not test_api.edit_algorithm_config(agent_info['appid'], plugin_id, "directory_userinput", "ignore"):
            print("[test] Fail in step 6")
            return False
        print("[test] wait for algorithm config apply to agent, sleep 1 heartbeat cycle")
        time.sleep(self.heartbeat_time)

        # step 7 测试是否正确关闭算法
        print("[test] testing if hook is switch off")
        test_path = agent_info['test-dir-path']
        user_agent = test_api.test_block_request(app_hostname, test_path)
        if user_agent is not False:
            print("[test] Fail in step 7")
            return False

        return True
        
    # 测试添加、修改、删除app
    def test_4(self):
        test_api = testAPI()

        # step 1 添加随机app
        rand_app_id = test_api.add_random_app()
        if rand_app_id is None:
            print("[test] Fail in step 1")
            return False

        # step 2 修改app信息
        if test_api.change_app_general_config(rand_app_id) is False:
            print("[test] Fail in step 2")
            return False

        # step 3 删除app
        if test_api.del_app(rand_app_id) is False:
            print("[test] Fail in step 3")
            return False
        
        return True

    def test_5(self):
        test_api = testAPI()

        # step 1 生成token
        token = test_api.get_new_token()
        # step 2 测试token生效
        if test_api.test_token(token) is False:
            print("[test] Fail in step 2")
            return False
        
        # step 3 删除token
        if test_api.del_token(token) is False:
            print("[test] Fail in step 3")
            return False

        # step 4 测试token失效
        if test_api.test_token(token) is True:
            print("[test] Fail in step 4")
            return False
        
        return True

if __name__ == '__main__':
    # unittest.main()
    test_all = testAll()
    if test_all.test_5():
        print("test 5 pass!")
    # for server_name in envConfig.rasp_agents:
    #     print("testing server:" + server_name)
    #     if test_all.test_1(server_name):
    #         print("test 1 pass!\n")
    #     if test_all.test_2(server_name):
    #         print("test 2 pass!\n")
    #     if test_all.test_3(server_name):
    #         print("test 3 pass!\n")

