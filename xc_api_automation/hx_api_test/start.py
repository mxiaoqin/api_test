import time
import os
import sys

sys.path.append(os.getcwd())
from core.core import *

case_key = hx_api_test_key
server_name_cn = '华星OA测试服务器'
run_patch = os.getcwd() + '/'
pid = os.getpid()

case = [
    'test_login.py',
    'test_approval_list.py',
]

if __name__ == "__main__":
    print(server_name_cn + " 脚本运行")
    update_status(case_key, pid)
    run_key = insert_run_key(case_key)
    for i in range(len(case)):
        print('运行用例: ' + case[i])
        run_case_serivce_py(run_patch + case[i],1)
        time.sleep(1)
    #notice_dingding(run_key, server_name_cn)
    print(server_name_cn + " 脚本完毕")