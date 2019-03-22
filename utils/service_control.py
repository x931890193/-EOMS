# encoding: utf-8
"""
Create on: 2018-09-24 下午7:58
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import subprocess
import time

# from utils.service_info import cklog
from utils.passwd import PASSWORD


def service_handler(server, mode, port):
    # print('echo ' + PASSWORD +' | sudo -S /bin/pidof {}'.format(server))
    result_by_name, pid = subprocess.getstatusoutput('echo ' + PASSWORD + ' | sudo -S /bin/pidof {}'.format(server))
    res = 0
    if result_by_name:
        result_by_port, pid = subprocess.getstatusoutput(
            'echo ' + PASSWORD + " | sudo -S /bin/ss -tnl | /usr/bin/awk '$4 ~/.*:%s$/{print $4}'" % port)
        print('echo ' + PASSWORD + " | sudo -S /bin/ss -tnl | /usr/bin/awk '$4 ~/.*:%s$/{print $4}'" % port)
        if result_by_port:
            return 0
        try:
            res, s = subprocess.getstatusoutput('echo ' + PASSWORD + ' | sudo -S service {} {}'.format(server, mode))
            time.sleep(0.1)
            return 1 if not res else 0
        except:
            return res


if __name__ == '__main__':
    service_handler("nginx", "start", "22")
