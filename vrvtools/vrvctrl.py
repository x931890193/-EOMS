#!/usr/bin/env python3
#coding:utf-8
#author:kk

import threading
from gorgeous.utils import *
from vrvtools import vrvservices

# 获取所有日志文件路径
def cklog(s):
    if not os.path.isdir(s.get("logdir")):
        return False
    shell = "ls -lh %s%s | awk '/^-.*/{print $5,$NF}' | awk -F '/' '{print $1,$NF}'" %(s.get('logdir'),s.get("logindex"))
    result,output = subprocess.getstatusoutput(shell)
    print(shell)
    if "cannot" in output  :
        return False
    logs = [ i.split() for i in output.split('\n')]
    logs.reverse()
    if len(logs) > 8 :
        logs = logs[0:7]
    s['logs'] = logs


# 通过pidof命令判断进程是否存在
def ckpid(s):
    result,output = subprocess.getstatusoutput('/bin/pidof %s'%s.get('name'))
    cklog(s)
    if result :
        s['status'] = "FAILED"
    else :
        s['status'] = "SUCCESS"
        s['pid'] = output


def ckjavapid(s):
    javadir = '/home/kali/Desktop/eoms/data/linkdood/im/IMServer/'
    pidfile = "%s/%s/%s.pid" %(javadir,s.get('name'),s.get('name'))
    cklog(s)
    if os.path.isfile(pidfile):
        s['status'] = "SUCCESS"
    else :
        s['status'] = "FAILED"

# 通过端口判断进程是否存在
def ckport(s) :
    result,output = subprocess.getstatusoutput("/bin/ss -tnl | /usr/bin/awk '$4~/.*:%s/{print $4}'"%s.get('port'))
    cklog(s)
    if output :
        s['status'] = "SUCCESS"
    else :
        s['status'] = "FAILED"


# 检查所有服务状态
def vrvcheck():
    th_list = [] # 存储所有服务查询进程
    for server in vrvservices.services.keys() :
        for s in vrvservices.services.get(server):
            if server == 'cpp' or (server == 'base' and s.get('name') in ('mysqld','redis-server','turnserver','fdfs_trackerd','fdfs_storaged','nginx')):
                th = threading.Thread(target=ckpid,args=(s,))  # 启动线程
                th.start()
                th_list.append(th)
            elif server == 'java' :
                th = threading.Thread(target=ckjavapid,args=(s,))
                th.start()
                th_list.append(th)
            elif s.get('name') in ('zookeeper','kafka','elasticsearch','tomcat-webapp','tomcat-app',):
                th = threading.Thread(target=ckport,args=(s,))
                th.start()
                th_list.append(th)
            else :
                pass

    for t in th_list:
       t.join()
    return vrvservices.services


def vrvctrl(name,ctrl):
    # 调用link 重启服务
    if name == "cj":
        name = 'all'
    elif name == "all" and ctrl == 'stop':
        ctrl = 'fstop'
    cmd = '/usr/bin/linked %s %s'%(name,ctrl)
    logger.info(cmd)
    result,output = subprocess.getstatusoutput(cmd)
    if ctrl == 'start':
        time.sleep(1)
    logger.debug('执行成功')
    return None


# 日志打包
def getlog(logdir,logs,downfile='vrvlog.zip'):
    if not os.path.isdir(logdir):
        return False
    os.chdir(logdir)

    logfile = os.path.join(DOWNLOG_DIR,downfile)
    
    if os.path.isfile(logfile):
        os.remove(logfile)
    cmd = '/usr/bin/zip -r %s ' %logfile
    for f in logs :
        cmd += '%s '%f

    logger.info('压缩命令 %s'%cmd)
    result,output = subprocess.getstatusoutput(cmd)
    if  result :
        return False
    return logfile



def updatectl():
    pass


if __name__ == "__main__" :
    vrvcheck()
