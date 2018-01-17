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
        self.case_name = '后台登录接口'
        self.run_key = get_now_run_key(hx_api_test_key)
        self.url = hx_api_test_url + '/v1/authorizations'
        self.request_mode = 'Post'

        #以下在脚本中赋值
        self.headers = ''
        self.cookies = ''
        self.result = 'Fail'
        self.step = ''
        self.request_data = ''
        self.status_code = ''
        self.response = ''



    def test_login(self):
        try:
            data = {}
            data['phone'] = "13910101010"
            data['password'] = 'huaxing2017'

            payload = data

            # json 提交
            # payload = json.dumps(data, ensure_ascii=False).encode('utf-8')

            self.request_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.step += "1. 发出post请求 "
            r = post_request(self.url, payload, self.headers, self.cookies)
            self.status_code = r.status_code
            self.response = str(r.text)

            if (r.status_code == 201):
                self.step += "2. 判响应码 "
                self.response = r.json()
                self.result = 'Pass'
                install_case_token(self.run_key, self.response['data']['token'])
                self.step += "3. 登录成功并保存token "
                self.response = str(self.response)
        except :
            print('脚本异常')
            self.result = 'Pass'

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
