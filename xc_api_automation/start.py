import datetime
import time
import sys
import os
from core.core import *

run_patch = os.getcwd()
sys.path.append(run_patch+'/')

pid = os.getpid()
case_key = 'task_server'


if __name__ == "__main__":
    while(True):
        try:
            update_status('task_server', os.getpid())
            task_list = get_task_list()
            for i in range(len(task_list)):
                run_status = get_run_status_by_case_key(task_list[str(i)]['case_key'])
                if(len(run_status) == 0):
                    run_status = install_status(task_list[str(i)]['case_key'])
                if(run_status == None or search_pid(run_status['case_pid'], task_list[str(i)]['interval'], run_status['update_time'])):
                    print('启动脚本: '+ run_status['case_name_cn'])
                    run_case_serivce_py(run_patch + task_list[str(i)]['run_patch'])
                    update_task_runtime(task_list[str(i)]['id'], task_list[str(i)]['interval'])
            print("线程休眠 5 秒")
            time.sleep(5)
        except :
            print('运行异常')
            time.sleep(5)

