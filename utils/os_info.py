# encoding: utf-8
"""
Create on: 2018-09-23 下午7:58
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import datetime
import json
import os
import time

import psutil
from django.db.models import Max, Min

from app_entry.models import Os_Info_Tmp, OS_Info_Static
from utils.passwd import PASSWORD
from utils.time import realtime


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.4f%s' % (value, s)
    return '%.2fB' % n


def get_os_info():
    netinfo = Os_Info_Tmp.objects.aggregate(Max("netin"), Max("netout"))
    os_version = os.popen('head -1 /etc/issue').readline().strip()
    cpu_total = psutil.cpu_count()
    mem_total = os.popen('free -h|grep "Mem"|awk \'{print $2}\'').readline().strip()
    uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%m-%d %H:%M:%S")
    disk_root = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $2}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/$"|awk \'{print $2}\'').readline().strip())
    disk_data = '0' if (os.popen(
        'df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $2}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $2}\'').readline().strip())
    disk_root_p = psutil.disk_usage('/').percent
    disk_data_p = psutil.disk_usage('/').percent
    disk_root_f = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $4}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/$"|awk \'{print $4}\'').readline().strip())
    disk_root_u = '0' if (os.popen('df -Ph|grep "/$"|awk \'{print $3}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/$"|awk \'{print $3}\'').readline().strip())
    disk_data_f = '0' if (os.popen(
        'df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $4}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $2}\'').readline().strip())
    disk_data_u = '0' if (os.popen(
        'df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $3}\'').readline().strip()) == '' else (
        os.popen('df -Ph|grep "/home/kali/Desktop/keke/data$"|awk \'{print $2}\'').readline().strip())
    login_num = int(os.popen('last | grep "still logged in"  | wc -l').readline().strip())
    proc_num = len(psutil.pids())
    net_conn = int(
        os.popen('echo ' + PASSWORD + ' | sudo -S netstat -anputl|grep "ESTABLISHED"|wc -l').readline().strip())
    ssh_status = 'On' if int(os.popen('ps -ef|grep sshd|wc -l').readline().strip()) > 0 else 'Off'
    with open('/proc/loadavg') as f:
        cpu_avg = f.read().split()
        cpu_1 = cpu_avg[0]
        cpu_5 = cpu_avg[1]
        cpu_15 = cpu_avg[2]
    memory = psutil.virtual_memory().percent
    swap = psutil.swap_memory().percent
    cpu = psutil.cpu_percent()
    
    netout = psutil.net_io_counters().bytes_sent
    netin = psutil.net_io_counters().bytes_recv
    if netinfo["netin__max"] is not None:
        netin_last = netin - netinfo["netin__max"]
    else:
        netin_last = 0
    if netinfo["netout__max"] is not None:
        netout_last = netout - netinfo["netout__max"]
    else:
        netout_last = 0
    return (cpu, cpu_1, cpu_5, cpu_15, memory, swap, netin, netout, netin_last,
            netout_last, os_version, int(cpu_total), mem_total,
            uptime, disk_root, disk_root_p, disk_root_f,
            disk_root_u, disk_data, disk_data_p, disk_data_f,
            disk_data_u, login_num, proc_num, net_conn, ssh_status
            )


def get_os_data():
    save_data()
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
    
    os_info = Os_Info_Tmp.objects.all()
    os_static = OS_Info_Static.objects.all().order_by("-in_time")[:10]
    par_info = OS_Info_Static.objects.aggregate(Min("cpu"), Max("cpu"), Min("cpu_1"),
                                                Max("cpu_1"), Min("cpu_5"), Max("cpu_5"), Min("cpu_15"), Max("cpu_15"),
                                                Min("memory"), Max("memory"), Min("swap"), Max("swap"), Min("netin"),
                                                Max("netin"), Min("netout"),
                                                Max("netout"))
    for row in os_static:
        time_x = datetime.datetime.strftime(row.in_time, '%H:%M')
        data_y1 = row.cpu
        data_y2 = row.cpu_1
        data_y3 = row.cpu_5
        data_y4 = row.cpu_15
        data_y5 = row.memory
        data_y6 = row.swap
        data_y7 = row.netin
        data_y8 = row.netout
        _time.append(time_x)
        data_cpu.append(data_y1)
        data_cpu1.append(data_y2)
        data_cpu5.append(data_y3)
        data_cpu15.append(data_y4)
        data_memory.append(data_y5)
        data_swap.append(data_y6)
        data_netin.append(round(data_y7 / 5 / 60, 2))
        data_netout.append(round(data_y8 / 5 / 60, 2))
    
    for i in os_info:
        Uptime = i.uptime
        Disk_Root = i.disk_root
        Disk_Root_p = i.disk_root_p
        Disk_Root_f = i.disk_root_f
        Disk_Root_u = i.disk_root_u
        Disk_Data = i.disk_data
        Disk_Data_p = i.disk_data_p
        Disk_Data_f = i.disk_data_f
        Disk_Data_u = i.disk_data_u
        Login = i.login_num
        Process = i.proc_num
        Connection = i.net_conn
        SSH = i.ssh_status
    
    cpu_min = par_info.get("cpu__min")
    cpu_max = par_info.get("cpu__max")
    cpu1_min = par_info.get("cpu_1__min")
    cpu1_max = par_info.get("cpu_1__max")
    cpu5_min = par_info.get("cpu_5__min")
    cpu5_max = par_info.get("cpu_5__max")
    cpu15_min = par_info.get("cpu_15__min")
    cpu15_max = par_info.get("cpu_15__max")
    memory_min = par_info.get("memory__min")
    memory_max = par_info.get("memory__max")
    swap_min = par_info.get("swap__min")
    swap_max = par_info.get("swap__max")
    netin_min = par_info.get("netin__min")
    netin_max = par_info.get("netin__max")
    netout_min = par_info.get("netout__min")
    netout_max = par_info.get("netout__max")
    
    OS = os_info[len(os_info) - 1].os_version
    CPUs = os_info[0].cpu_total
    Memory = os_info[0].mem_total
    
    cpu_data['labels'] = json.dumps(_time[::-1])
    cpu_data['data'] = json.dumps(data_cpu)
    cpu_data['max'] = cpu_max
    cpu_data['min'] = cpu_min
    cpu_load_data['labels'] = json.dumps(_time[::-1])
    cpu_load_data['data'] = json.dumps([data_cpu1, data_cpu5, data_cpu15])
    cpu_load_data['cpu1_max'] = cpu1_max
    cpu_load_data['cpu1_min'] = cpu1_min
    cpu_load_data['cpu5_max'] = cpu5_max
    cpu_load_data['cpu5_min'] = cpu5_min
    cpu_load_data['cpu15_max'] = cpu15_max
    cpu_load_data['cpu15_min'] = cpu15_min
    memory_data['labels'] = json.dumps(_time[::-1])
    memory_data['data'] = json.dumps([data_memory, data_swap])
    memory_data['memory_max'] = memory_max
    memory_data['memory_min'] = memory_min
    memory_data['swap_max'] = swap_max
    memory_data['swap_min'] = swap_min
    net_data['labels'] = json.dumps(_time[::-1])
    net_data['data'] = json.dumps([data_netin, data_netout])
    net_data['netin_max'] = bytes2human(netin_max / 5 / 60)
    net_data['netin_min'] = bytes2human(netin_min / 5 / 60)
    net_data['netout_max'] = bytes2human(netout_max / 5 / 60)
    net_data['netout_min'] = bytes2human(netout_min / 5 / 60)
    
    Swap_Memory = os.popen('free -h|grep "Swap"|awk \'{print $2}\'').readline().strip()
    user = psutil.users()[0].name
    NOW = datetime.datetime.now()
    # print(NOW.strftime("%Y%m%d%H%M%S"))
    os.popen("top -n 1 -b  > ./tmp/{}.txt".format(NOW.strftime("%Y%m%d%H%M%S")))
    time.sleep(0.2)
    try:
        with open("./tmp/{}.txt".format(NOW.strftime("%Y%m%d%H%M%S")), "r") as f:
            s = f.readlines()[7:30]
        alist = []
        blist = []
        for i in s:
            tmp = i.split(" ")
            alist.append([val for val in tmp if val])
        for j in alist:
            blist.append({
                "PID":  j[0], "USER": j[1], "PR": j[2],
                "NI":   j[3], "VIRT": j[4], "RES": j[5],
                "SHR":  j[6], "S": j[7], "CPU": j[8], "MEM": j[9],
                "TIME": j[10], "COMMAND": " ".join(j[11:])
            })
        is_ok = True if blist else False
    except:
        is_ok = False
    return_data = {
        'cpu':         cpu_data, 'cpuload': cpu_load_data, 'mem': memory_data, 'net': net_data,
        'OS':          OS, 'CPUs': CPUs, 'Memory': Memory, 'Uptime': Uptime, 'Disk_Root': Disk_Root,
        'Disk_Root_p': Disk_Root_p, 'Disk_Root_f': Disk_Root_f, 'Disk_Root_u': Disk_Root_u,
        'Disk_Data':   Disk_Data, 'Disk_Data_p': Disk_Data_p, 'Disk_Data_f': Disk_Data_f,
        'Disk_Data_u': Disk_Data_u, 'Login': Login, 'Process': Process, 'Connection': Connection,
        'SSH':         SSH, "Swap_Memory": Swap_Memory, "user": user, "time": realtime().get("time"),
        "is_ok":       is_ok, "process_data": blist,
    }
    
    return return_data


def save_data():
    data = get_os_info()
    Os_Info_Tmp.objects.create(
        os_version=data[10], cpu_total=data[11], mem_total=data[12],
        uptime=data[13], disk_root=data[14], disk_root_p=data[15],
        disk_root_f=data[16], disk_root_u=data[17], disk_data=data[18],
        disk_data_p=data[19], disk_data_f=data[20], disk_data_u=data[21],
        login_num=data[22], proc_num=data[23], net_conn=data[24],
        ssh_status=data[25], netin=data[6], netout=data[7]
    )
    
    OS_Info_Static.objects.create(
        cpu=data[0], cpu_1=data[1], cpu_5=data[2], cpu_15=data[3],
        memory=data[4], swap=data[5], netin=data[6], netout=data[7],
        user=",".join([val.name for val in psutil.users()])
    )
