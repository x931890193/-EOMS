# encoding: utf-8
"""
Create on: 2018-09-24 下午3:37
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import os
import subprocess
# 获取所有日志文件路径
import threading

from utils.services import services


def cklog(s):
    if not os.path.isdir(s.get("logdir")):
        return False
    shell = "ls -lh %s%s | awk '/^-.*/{print $5,$NF}' | awk -F '/' '{print $1,$NF}'" % (
        s.get('logdir'), s.get("logindex"))
    result, output = subprocess.getstatusoutput(shell)
    if "cannot" in output:
        return False
    logs = [i.split() for i in output.split('\n')]
    logs.reverse()
    if len(logs) > 8:
        logs = logs[0:7]
    s['logs'] = logs


# 通过pidof命令判断进程是否存在
def ckpid(s):
    result, output = subprocess.getstatusoutput('/bin/pidof %s' % s.get('name'))
    cklog(s)
    if result:
        s['status'] = "FAILED"
    else:
        s['status'] = "SUCCESS"
        s['pid'] = output


def ckjavapid(s):
    javadir = '/home/kali/Desktop/keke/data/linkdood/im/IMServer/'
    pidfile = "%s/%s/%s.pid" % (javadir, s.get('name'), s.get('name'))
    cklog(s)
    if os.path.isfile(pidfile):
        s['status'] = "SUCCESS"
    else:
        s['status'] = "FAILED"


# 通过端口判断进程是否存在
def ckport(s):
    result, output = subprocess.getstatusoutput("/bin/ss -tnl | /usr/bin/awk '$4~/.*:%s$/{print $4}'" % s.get('port'))
    cklog(s)
    if output:
        s['status'] = "SUCCESS"
    else:
        s['status'] = "FAILED"


# 检查所有服务状态
def vrvcheck():
    th_list = []  # 存储所有服务查询进程
    for server in services.keys():
        for s in services.get(server):
            s["port"] = s.get("port")
            if server == 'cpp' or (server == 'base' and s.get('name') in ('redis-server', 'turnserver',
                                                                          'fdfs_trackerd', 'fdfs_storaged', 'nginx')):
                th = threading.Thread(target=ckpid, args=(s,))  # 启动线程
                th.start()
                th_list.append(th)
            elif server == 'java':
                th = threading.Thread(target=ckjavapid, args=(s,))
                th.start()
                th_list.append(th)
            elif s.get('name') in ('zookeeper', 'mysql', 'kafka', "mongodb",
                                   "apache2", 'elasticsearch', 'tomcat-webapp',
                                   'tomcat-app',):
                th = threading.Thread(target=ckport, args=(s,))
                th.start()
                th_list.append(th)
            else:
                pass
    
    for t in th_list:
        t.join()
    
    return services


if __name__ == '__main__':
    vrvcheck()
