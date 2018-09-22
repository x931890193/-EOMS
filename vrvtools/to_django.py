#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import psutil
import json
import datetime
import os
import pymysql
def conn_database():
    '''连接数据库'''
    global db_conn
    global db_curs
    global db_name
    # db_name = '/home/kali/Desktop/eoms/vrvtools/to_django.db'
    # connect("localhost", "root", input("passwd:"), charset="utf8")
    try:
        # db_conn = sqlite3.connect(db_name)
        db_conn = pymysql.connect("localhost", "root", "flzx3qc", "demo", charset="utf8")
        db_curs = db_conn.cursor()
    except:
        print('DB Connect Error !!!')

#     t_os_info ="""create table if not exists t_os_info (
#   id          INTEGER PRIMARY KEY AUTO_INCREMENT,
#   in_time     DATETIME,
#   os_version  VARCHAR(30),
#   cpu_total   int,
#   mem_total   VARCHAR(30),
#   uptime      VARCHAR(30),
#   disk_root   VARCHAR(30),
#   disk_root_p VARCHAR(30),
#   disk_root_f VARCHAR(30),
#   disk_root_u VARCHAR(30),
#   disk_data   VARCHAR(30),
#   disk_data_p VARCHAR(30),
#   disk_data_f VARCHAR(30),
#   disk_data_u VARCHAR(30),
#   login_num   int,
#   proc_num    int,
#   net_conn    int,
#   ssh_status  VARCHAR(30),
#   netin       int,
#   netout      int
# )
#     t_os_statistic = """create table if not exists t_os_statistic (
#   id      INTEGER PRIMARY KEY auto_increment,
#   in_time TIMESTAMP default CURRENT_TIMESTAMP,
#   cpu     int,
#   cpu_1   int,
#   cpu_5   int,
#   cpu_15  int,
#   memory  int,
#   swap    int,
#   netin   int,
#   netout  int
# )"""
#     try:
#         db_curs.execute(t_os_info)
#         db_curs.execute(t_os_statistic)
#     except:
#         print('Table Init Error !!!')


def close_database():
    '''关闭数据库'''
    try:
        db_curs.close(), db_conn.commit(), db_conn.close()
    except:
        print('DB Close Error !!!')


def to_str(par):
    return '"' + par + '"'


def get_os_info():
    '''获取最新系统信息，并插入到data_source,次/分钟'''
    conn_database()
    try:
        sql_select = 'select max(netin),max(netout) from t_os_info;'
        db_curs.execute(sql_select)
        netinfo = db_curs.fetchone()

    except BaseException as e:
        print('Get Net_Info Error !!!', e)
    os_version = os.popen('head -1 /etc/issue').readline().strip()
    cpu_total = psutil.cpu_count()
    mem_total = os.popen('free -h|grep "Mem"|awk \'{print $2}\'').readline().strip()
    uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d,%H:%M:%S")
    disk_root = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $2}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/$"|awk \'{print $2}\'').readline().strip())
    disk_data = '0' if (os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $2}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $2}\'').readline().strip())
    disk_root_p = psutil.disk_usage('/').percent
    disk_data_p = psutil.disk_usage('/home/kali/Desktop/eoms/data').percent
    disk_root_f = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $4}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/$"|awk \'{print $4}\'').readline().strip())
    disk_root_u = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $3}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/$"|awk \'{print $3}\'').readline().strip())
    disk_data_f = '0' if (os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $4}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $2}\'').readline().strip())
    disk_data_u = '0' if (os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $3}\'').readline().strip()) == ''else (
        os.popen('df -Ph|grep "/home/kali/Desktop/eoms/data$"|awk \'{print $2}\'').readline().strip())
    login_num = int(os.popen('last | grep "still logged in"  | wc -l').readline().strip())
    proc_num = len(psutil.pids())
    net_conn = int(os.popen('netstat -anputl|grep "ESTABLISHED"|wc -l').readline().strip())
    ssh_status = 'On' if int(os.popen('ps -ef|grep sshd|wc -l').readline().strip()) > 0 else 'Off'
    with open('/proc/loadavg') as f:
        cpu_avg = f.read().split()
        cpu_1 = to_str(cpu_avg[0])
        cpu_5 = to_str(cpu_avg[1])
        cpu_15 = to_str(cpu_avg[2])
    memory = psutil.virtual_memory().percent
    swap = psutil.swap_memory().percent
    cpu = psutil.cpu_percent()

    netout = psutil.net_io_counters().bytes_sent
    netin = psutil.net_io_counters().bytes_recv
    
    if netinfo[0] is not None:
        netin_last = netin - netinfo[0]
    else:
        netin_last = 0
    if netinfo[1] is not None:
        netout_last = netout - netinfo[1]
    else:
        netout_last = 0

    return cpu, cpu_1, cpu_5, cpu_15, memory, swap, netin, netout, netin_last, netout_last, \
           to_str(os_version), int(cpu_total), to_str(mem_total), to_str(uptime), to_str(
        disk_root), disk_root_p, to_str(disk_root_f), to_str(disk_root_u), \
           to_str(disk_data), disk_data_p, to_str(disk_data_f), to_str(
        disk_data_u), login_num, proc_num, net_conn, to_str(ssh_status)


def insert_data():
    os_info = get_os_info()
    try:
        print('%s: generate_insert_data----' % time.ctime())
        delete_of_info = "delete from  t_os_info order by in_time limit 1"
        insert_os_info = "insert into t_os_info(os_version,cpu_total, mem_total, uptime, " \
                         "disk_root,disk_root_p,disk_root_f,disk_root_u,disk_data, disk_data_p, disk_data_f, disk_data_u, login_num, proc_num, net_conn, ssh_status,netin,netout)" \
                         " values(%s,%d,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s,%d,%d,%d,%s,%d,%d)" % \
                         (os_info[10], os_info[11], os_info[12], os_info[13], os_info[14], os_info[15],
                          os_info[16], os_info[17], os_info[18], os_info[19],
                          os_info[20], os_info[21], os_info[22], os_info[23],
                          os_info[24], os_info[25], os_info[6], os_info[7])
        # print(os_info[6])
        insert_os_statistic = "insert into t_os_statistic(cpu,cpu_1,cpu_5,cpu_15 ,memory ,swap ,netin ,netout  ) VALUES(%d,%s,%s,%s,%d,%d,%d,%d)" % (
            os_info[0], os_info[1], os_info[2], os_info[3], os_info[4], os_info[5], os_info[8], os_info[9])
        # print(os_info[8])
        db_curs.execute(delete_of_info)
        db_curs.execute(insert_os_info)
        db_curs.execute(insert_os_statistic)
    except BaseException as e:
        print('Insert  Data Error !!!', e)
    finally:
        close_database()


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


def check_data():
    conn_database()
    get_info_count = "select count(*) from t_os_info"
    get_data_count = "select count(*) from t_os_statistic"
    db_curs.execute(get_info_count)
    get_info_rows = db_curs.fetchone()
    db_curs.execute(get_data_count)
    get_data_rows = db_curs.fetchone()
    # print(get_info_rows[0],get_data_rows[0], 66666666)
    # if get_info_rows[0] <= 1  or get_data_rows[0] == 0:
    insert_data()


def get_data(parameter='default', time='-1 hour'):
    check_data()
    conn_database()
    get_os = 'select os_version,cpu_total, mem_total, uptime,disk_root,disk_root_p,disk_root_f,disk_root_u,disk_data, disk_data_p, disk_data_f, disk_data_u, login_num, proc_num, net_conn, ssh_status from t_os_info'
    #get_all = 'select  strftime(\'%H:%M\',in_time),cpu,cpu_1,cpu_5,cpu_15,memory,swap,netin,netout from t_os_statistic where in_time > datetime(\'now\',\'localtime\',\'' + time + '\') limit 12 offset (select count(*) from t_os_statistic)-12'
    # a = datetime.strftime()
    # print(a)
    # get_all = 'select strftime(\'%H:%M\',in_time),cpu,cpu_1,cpu_5,cpu_15,memory,swap,netin,netout from t_os_statistic limit 12 offset '
    get_all = 'select in_time,cpu,cpu_1,cpu_5,cpu_15,memory,swap,netin,netout from t_os_statistic limit 15 offset '
    # get_te
    # get_min = 'select  min(cpu),max(cpu),min(cpu_1),max(cpu_1),min(cpu_5),max(cpu_5),min(cpu_15),max(cpu_15),min(memory),max(memory),min(swap),max(swap),min(netin),max(netin),min(netout),max(netout) from t_os_statistic  where in_time > datetime(\'now\',\'localtime\', \'' + time + '\')'
    get_offest = 'select count(*) from t_os_statistic;'
    get_min = 'select  min(cpu),max(cpu),min(cpu_1),max(cpu_1),min(cpu_5),max(cpu_5),min(cpu_15),max(cpu_15),' \
              'min(memory),max(memory)' \
              ',min(swap),max(swap),min(netin),max(netin),min(netout),max(netout) from (select * from t_os_statistic ' \
              'limit 15 offset'
    cpu_data = {}
    cpu_load_data = {}
    memory_data = {}
    net_data = {}
    _time = []
    data_cpu = []
    data_cpu1 = []
    data_cpu5 = []
    data_cpu15 = []
    data_memory = []
    data_swap = []
    data_netin = []
    data_netout = []
    try:
        
        db_curs.execute(get_os)
        os_info = db_curs.fetchone()
        
        db_curs.execute(get_offest)
 
        os_temp = db_curs.fetchone()[0]
        # print(get_min + " " + str(os_temp) + " as s")
        tmp = os_temp - 12
        # print(get_min + " " + str(os_temp) + "-12 ) as s")
        db_curs.execute(get_min + " " + str(tmp) + " ) as s")
        
     
        par_info = db_curs.fetchone()
        db_curs.execute(get_all + " " + str(tmp))
        data_info = db_curs.fetchall()
        # print(777777)
        # time = []
        for row in data_info:
            # print(type(row[0]))
            time_x = datetime.datetime.strftime(row[0], '%H:%M')
            # print(time_x)
            # time_x = row[0]
            data_y1 = row[1]
            data_y2 = row[2]
            data_y3 = row[3]
            data_y4 = row[4]
            data_y5 = row[5]
            data_y6 = row[6]
            data_y7 = row[7]
            data_y8 = row[8]
            _time.append(time_x)
            data_cpu.append(data_y1)
            data_cpu1.append(data_y2)
            data_cpu5.append(data_y3)
            data_cpu15.append(data_y4)
            data_memory.append(data_y5)
            data_swap.append(data_y6)
            data_netin.append(round(data_y7 / 5 / 60, 2))
            data_netout.append(round(data_y8 / 5 / 60, 2))
    except BaseException as e:
        print('Get Para_MIN Error !!!', e)
   
    OS = os_info[0][0:-4]
    CPUs = os_info[1]
    Memory = os_info[2]

    Uptime = os_info[3][5:]
    # Uptime = datetime.datetime.strftime(os_info[3], '%M:%S')
    # print(Uptime)
    Disk_Root = os_info[4]
    Disk_Root_p = os_info[5]
    Disk_Root_f = os_info[6]
    Disk_Root_u = os_info[7]
    Disk_Data = os_info[8]
    Disk_Data_p = os_info[9]
    Disk_Data_f = os_info[10]
    Disk_Data_u = os_info[11]
    Login = os_info[12]
    Process = os_info[13]
    Connection = os_info[14]
    SSH = os_info[15]
    
    cpu_min = par_info[0]
    cpu_max = par_info[1]
    cpu1_min = par_info[2]
    cpu1_max = par_info[3]
    cpu5_min = par_info[4]
    cpu5_max = par_info[5]
    cpu15_min = par_info[6]
    cpu15_max = par_info[7]
    memory_min = par_info[8]
    memory_max = par_info[9]
    swap_min = par_info[10]
    swap_max = par_info[11]
    netin_min = par_info[12]
    netin_max = par_info[13]
    netout_min = par_info[14]
    netout_max = par_info[15]
    # print(_time, 666666666)
    cpu_data['labels'] = json.dumps(_time)
    cpu_data['data'] = json.dumps(data_cpu)
    cpu_data['max'] = cpu_max
    cpu_data['min'] = cpu_min
    cpu_load_data['labels'] = json.dumps(_time)
    cpu_load_data['data'] = json.dumps([data_cpu1, data_cpu5, data_cpu15])
    cpu_load_data['cpu1_max'] = cpu1_max
    cpu_load_data['cpu1_min'] = cpu1_min
    cpu_load_data['cpu5_max'] = cpu5_max
    cpu_load_data['cpu5_min'] = cpu5_min
    cpu_load_data['cpu15_max'] = cpu15_max
    cpu_load_data['cpu15_min'] = cpu15_min
    memory_data['labels'] = json.dumps(_time)
    memory_data['data'] = json.dumps([data_memory, data_swap])
    memory_data['memory_max'] = memory_max
    memory_data['memory_min'] = memory_min
    memory_data['swap_max'] = swap_max
    memory_data['swap_min'] = swap_min
    net_data['labels'] = json.dumps(_time)
    net_data['data'] = json.dumps([data_netin, data_netout])
    net_data['netin_max'] = bytes2human(netin_max / 5 / 60)
    net_data['netin_min'] = bytes2human(netin_min / 5 / 60)
    net_data['netout_max'] = bytes2human(netout_max / 5 / 60)
    net_data['netout_min'] = bytes2human(netout_min / 5 / 60)

    


    return_data = {'cpu': cpu_data, 'cpuload': cpu_load_data, 'mem': memory_data, 'net': net_data, 'OS': OS,
                   'CPUs': CPUs, 'Memory': Memory, 'Uptime': Uptime, 'Disk_Root': Disk_Root, 'Disk_Root_p': Disk_Root_p,
                   'Disk_Root_f': Disk_Root_f, 'Disk_Root_u': Disk_Root_u, 'Disk_Data': Disk_Data,
                   'Disk_Data_p': Disk_Data_p, 'Disk_Data_f': Disk_Data_f, 'Disk_Data_u': Disk_Data_u, 'Login': Login,
                   'Process': Process, 'Connection': Connection, 'SSH': SSH}

    return return_data


if __name__ == '__main__':
    insert_data()
    # get_data()
    # print(get_os_info() )
