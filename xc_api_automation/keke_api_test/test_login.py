import unittest
import sys
import os
import time
import json
sys.path.append(os.getcwd()+'/')

from core.core import *


class Test_login(unittest.TestCase):

    def setUp(self):
        #必须更改
        self.case_name = 'APP登录接口'
        self.run_key = get_now_run_key(keke_key)
        self.url = keke_url + '/v1/portal/login'
        self.request_mode = 'Post'

        # 以下在脚本中赋值
        self.headers = ''
        self.cookies = ''
        self.result = 'Fail'
        self.step = ''
        self.request_data = ''
        self.status_code = ''
        self.response = ''



    def test_login(self):

        data = {}
        data['phone'] = "18611701565"
        data['passwd'] = '123456'
        data['client'] = 'android'
        data['device'] = 'awfwafwefawefwaef33d'

        payload = data
        #payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.request_data = str(payload)
        self.step += '1. 发出post请求/n'
        r = post_request(self.url, payload, self.headers, self.cookies)
        self.status_code = r.status_code
        self.response = str(r.text)
        if(r.status_code == 200):
            self.step += '2. 接口访问正常,响应吗正确/n'
            self.response = r.json()
            if(self.response['status'] == '4000002'):
                self.step += '3. 结果验证成功/n'
                self.result = 'Pass'
                self.response = str(r.json())
            self.response = str(r.json())

    def tearDown(self):
        insert_api_log(self.run_key,
                       self.case_name,
                       self.request_mode,
                       self.url,
                       self.result,
                       self.request_data,
                       self.response,
                       self.status_code,
                       self.step)


if __name__ =='__main__':
  unittest.main()
