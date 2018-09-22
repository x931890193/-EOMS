#_*_ending:utf-8_*_

from gorgeous.utils import *

def start(change=1):
    if change == 1:
        sshd_status = subprocess.getstatusoutput("service sshd start")
    if sshd_status[0] == 0:
        return True
    else:
        return False

def stop(change=0):
    if change == 0:
        sshd_status = subprocess.getstatusoutput("service sshd stop")
    if sshd_status[0] == 0:
        return True
    else:
        return False


def check(change="check"):
    sshd_status = subprocess.getstatusoutput("service sshd status")
    print(sshd_status)
    if sshd_status[0] != 0 or change != "check":
        return False        ##  sshd 服务器未启动  或者 输入的不是 check
    elif sshd_status[0] == 0:
        sshd_pid = re.search("\S[0-9]\S+", sshd_status[1])
        sshd_pid = sshd_pid.group()
        # print(sshd_pid,6666666)
        sshd_process = subprocess.getstatusoutput("netstat -nltp| grep %s|awk '{print $4}'|awk -F':' '{print $NF }'|uniq" % (sshd_pid))
        sshd_process = subprocess.getstatusoutput("netstat -nltp| grep sshd|awk '{print $4}'|awk -F':' '{print $NF "
                                                  "}'|uniq" % (sshd_pid))
        # print(sshd_process)
        # sshd_process[1] = 22
        # return sshd_process[1]
        return 22

def modifi(change=10022):
    if change > 10000 and change <65535:
        monitor_port = subprocess.getstatusoutput("netstat -nltp| grep :%s" % (change))
        sshd_status = subprocess.getstatusoutput("service sshd status")
        if monitor_port[0] == 0 or sshd_status[0] != 0:
            return False        ##  将要修改的 端口被占用 或 sshd 服务未启动
        else:
            sshd_pid = re.search("[0-9]+", sshd_status[1])
            sshd_pid = sshd_pid.group()
            port_type = subprocess.getstatusoutput("grep '^#Port.*' /etc/ssh/sshd_config")
            if port_type[0] == 0:
                result = subprocess.getstatusoutput("sed -i '/^#Port.*/s@^#Port.*@Port %s@' /etc/ssh/sshd_config" % (change))
            else:
                result = subprocess.getstatusoutput("sed -i '/^Port.*/s@^Port.*@Port %s@' /etc/ssh/sshd_config" % (change))
            if result[0] == 0:
                sshd_process = subprocess.getstatusoutput(" netstat -nltp| grep %s|awk '{print $4}'|awk -F':' '{print $NF }'|uniq" % (sshd_pid))
                active_port = str(sshd_process[1])
                change = str(change)
                with open("/etc/sysconfig/iptables", "r", encoding="utf-8") as fr:
                    file_old = fr.readlines()
                    file_new = []
                    for line in file_old:
                        if active_port in line:
                            line = re.sub(active_port,change,line,count=1)
                            file_new.append(line)
                        else:
                            file_new.append(line)
                    with open("/etc/sysconfig/iptables", "w+", encoding="utf-8") as fw:
                        for line in file_new:
                            fw.write(line)
                    subprocess.getstatusoutput("service sshd restart")
                    subprocess.getstatusoutput("service iptables reload")
                    return True
    else:
        return False

if __name__ == "__main__":
    Mod = sys.argv[1]
    ssh = start_sshd(Mod)

