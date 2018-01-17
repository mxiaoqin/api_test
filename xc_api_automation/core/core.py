import subprocess
import time
import requests
from requests.adapters import HTTPAdapter
import pymysql
import json

from core.constants import *


def get_conn():
    conn = pymysql.connect(
        host='47.94.104.82',
        port=3306,
        user='qalog',
        passwd='OmHpPL7YON408E7h',
        db='qalog',
        charset='utf8',
    )
    return conn


# 获取任务列表
def get_task_list():
    task_list = {}
    conn = ''
    cursor = ''
    run_time = get_timenow()
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # print("SELECT * FROM `run_task` WHERE if_run = 0 AND run_time <='"+ run_time + "'")
        cursor.execute("SELECT * FROM `run_task` WHERE if_run = 0 AND run_time <='" + run_time + "'")
        data = cursor.fetchall()
        for i in range(len(data)):
            data1 = {}
            data1['id'] = data[i][0]
            data1['case_key'] = data[i][1]
            data1['interval'] = data[i][2]
            data1['run_time'] = int(data[i][3].timestamp())
            data1['type'] = data[i][4]
            data1['run_patch'] = data[i][5]
            task_list[str(i)] = data1
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return task_list


# 获取运行状态
def get_run_status_by_case_key(case_key):
    run_status = {}
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT * FROM `run_status` WHERE case_key='" + case_key + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in range(len(data)):
            data1 = {}
            data1['id'] = data[i][0]
            data1['update_time'] = int(data[i][1].timestamp())
            data1['case_key'] = data[i][2]
            data1['case_name_cn'] = data[i][3]
            data1['case_pid'] = data[i][4]
            run_status = data1
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return run_status


# 获取当前时间 默认不传参数 返回时间格式 传1 返回时间戳
def get_timenow(type=0):
    if (type == 1):
        return int(time.time())
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    return update_time


# 更新定时任务时间
def update_task_runtime(id, interval):
    update_timne = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()) + interval))
    sql = "UPDATE `run_task` SET `run_time`=%s WHERE (`id`=%s);"
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (update_timne, id))
        conn.commit()
    except pymysql.Error as e:
        print("update" + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()


# 更新服务状态
def update_status(case_key, pid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        update_time = get_timenow()
        cursor.execute("SELECT * FROM `run_status` WHERE if_delete = 0 and case_key='" + case_key + "'")
        data = cursor.fetchone()
        if (data is not None):
            sql = "UPDATE `run_status` SET `update_time`=%s, `case_pid`=%s WHERE (`id`=%s);"
            cursor.execute(sql, (update_time, pid, data[0]))
        else:
            case_name_cn = case_name_cn_list[case_key]
            sql = "INSERT INTO run_status (update_time,case_key,case_name_cn,case_pid,if_delete) VALUES(%s,%s,%s,%s,%s);"
            cursor.execute(sql, (update_time, case_key, case_name_cn, pid, 0))
        conn.commit()
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()


# 更新服务状态
def install_status(case_key):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        update_time = get_timenow()
        case_name_cn = case_name_cn_list[case_key]
        sql = "INSERT INTO run_status (update_time,case_key,case_name_cn,case_pid,if_delete) VALUES(%s,%s,%s,%s,%s);"
        cursor.execute(sql, (update_time, case_key, case_name_cn, -1, 0))
        data1 = {}
        data1['id'] = int(cursor.lastrowid)
        data1['update_time'] = update_time

        data1['case_key'] = case_key
        data1['case_name_cn'] = case_name_cn
        data1['case_pid'] = 0
        conn.commit()
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return data1


# 插入api log
def insert_api_log(run_key, case_name, request_mode, url, result, request_data, response_data, status_code, case_step):
    stime = get_timenow()
    print('run_key' + run_key)

    sql = "INSERT INTO automation_api_log (run_key, case_name, request_mode, url,result,request_data, response_data, status_code,create_time,case_step) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # print(sql)
        cursor.execute(sql, (
        run_key, case_name, request_mode, url, result, request_data, response_data, status_code, stime, case_step))
        conn.commit()
    except pymysql.Error as e:
        print("insert" + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()


def get_run_key():
    return time.strftime('%Y%m%d%H%M%S')


# 插入run key
def insert_run_key(case_key):
    stime = get_timenow()
    sql = "INSERT INTO run_key (run_key, case_key, create_time) VALUES(%s,%s,%s);"
    conn = ''
    cursor = ''
    run_key = get_run_key()
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (run_key, case_key, stime))
        conn.commit()
    except pymysql.Error as e:
        print("insert" + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return run_key


def get_now_run_key(case_key):
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT run_key FROM run_key WHERE case_key = '" + case_key + "' ORDER BY create_time DESC LIMIT 1"
        cursor.execute(sql)
        data = cursor.fetchall()

    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return data[0][0]


def update_run_key_token(run_key, token):
    sql = "UPDATE `run_key` SET `token`=%s WHERE (`run_key`=%s);"
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (token, run_key))
        conn.commit()
    except pymysql.Error as e:
        print("update" + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()


# kill pid
def kill_pid(pid):
    cmd = 'kill -9 ' + str(pid)
    subprocess.Popen(cmd, shell=True)


# 查询pid是否运行
def search_pid(pid, interval, update_time):
    if (pid == 0):
        return True
    run_switch = False
    time_now = get_timenow(1)
    cmd = 'tasklist|findstr ' + str(pid)
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    child.wait()
    cmd_response = str(child.stdout.read())
    cmd_response_list = cmd_response.split('\\n')
    for i in range(len(cmd_response_list)):
        cmd_response = cmd_response_list[i].split()
        if (len(cmd_response) > 1):
            if (cmd_response[1] == str(pid)):
                run_switch = True
        if (run_switch):
            break

    if (run_switch):
        # 检测是否假死
        if (update_time + interval + 7200 < time_now):
            kill_pid(pid)
            return True
        return False
    return True


# 运行case service python3
def run_case_serivce_py(patch, wait=0):
    cmd = 'python ' +patch
    child = subprocess.Popen(cmd, shell=True)
    if (wait == 1):
        child.wait()


# get
def get_request(url, payload, headers, cookies):
    try:
        r = requests.get(url, params=payload, headers=headers, cookies=cookies, timeout=10)
        return r
    except requests.HTTPError as e:
        print(e)
        return None


# post
def post_request(url, payload, headers, cookies):
    try:
        r = requests.post(url, data=payload, headers=headers, cookies=cookies, timeout=10)
        return r
    except requests.HTTPError as e:
        print(e)
        return None


# 获取日志 by run_key
def get_api_log_by_run_key(run_key):
    automation_api_log = {}
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT * FROM `automation_api_log` WHERE result = 'Fail' AND run_key='" + run_key + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in range(len(data)):
            data1 = {}
            data1['case_name'] = data[i][2]
            data1['url'] = data[i][4]
            data1['status_code'] = data[i][8]
            automation_api_log[str(i)] = data1
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()
    return automation_api_log


def notice_dingding(run_key, server_name_cn):
    log_list = get_api_log_by_run_key(run_key)
    if (len(log_list) == 0):
        return None
    data = {}
    data['msgtype'] = "markdown"
    markdown = {}
    markdown['title'] = server_name_cn + '报警 ' + run_key
    markdown['text'] = server_name_cn + " 查询key:" + run_key + "\n\n"
    for i in range(0, len(log_list)):
        tmp = ''
        tmp += "用例名称: " + log_list[str(i)]['case_name'] + "\n\n  url: " + log_list[str(i)][
            'url'] + "  error_code: " + str(log_list[str(i)]['status_code']) + "\n\n"
        tmp += "   \r\n"
        markdown['text'] = markdown['text'] + tmp
    data['markdown'] = markdown
    at = {}
    at['atMobiles'] = []
    at['isAtAll'] = False
    data['at'] = at
    payload1 = json.dumps(data, ensure_ascii=False).encode('utf-8')
    headerIe = {
        "Content-Type": "application/json"
    }
    r = post_request(
        'https://oapi.dingtalk.com/robot/send?access_token=a81fcd62c0f3572983bf5b4c78560999ce2cc37554ff2df8e9feda0b4f474a9a',
        payload1, headerIe, '')
    return r


def install_case_token(run_key, token):
    sql = "INSERT INTO case_token (run_key, token) VALUES(%s,%s);"
    conn = ''
    cursor = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (run_key, token))
        conn.commit()
    except pymysql.Error as e:
        print("insert" + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()


def get_case_token(run_key):
    conn = ''
    cursor = ''
    mm = ''
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT token FROM case_token WHERE run_key ='" + run_key + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        if conn:
            cursor.close()
            conn.close()

    if len(data) > 0:
         mm =data[0][0]
    else:
        print("data数据为空！")
    return mm
