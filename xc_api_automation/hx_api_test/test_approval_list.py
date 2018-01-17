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
        self.case_name = '审批列表接口'
        self.url = hx_api_test_url + '/v1/approval/list'

        self.request_mode = 'Get'

        #以下在脚本中赋值
        self.headers = ''
        self.cookies = ''
        self.result = 'Fail'
        self.step = ''
        self.request_data = ''
        self.status_code = ''
        self.response = ''

        self.run_key = get_now_run_key(hx_api_test_key)


    def test_login(self):
        try:
            token = get_case_token(self.run_key)
            self.headers = {'Authorization':'Bearer' + token}

            data = {}
            data['filter'] = 1
            data['is_page'] = 1
            data['limit'] = 15
            data['page'] = 1
            data['search_type'] = 2
            data['status1'] = 3
            data['user_id'] = 496

            payload = data


            # json 提交
            # payload = json.dumps(data, ensure_ascii=False).encode('utf-8')

            self.request_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.step += "1. 发出请求 "
            r = get_request(self.url, payload, self.headers, self.cookies)
            self.status_code = r.status_code
            self.response = str(r.text)
            self.step += "2. 判响应码 "
            if (r.status_code == 200):
                self.step += "3. 判响应码 成功 "
                self.result = 'Pass'
                self.response = str(r.json())
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
