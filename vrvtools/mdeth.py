#!/usr/bin/env python3
#
#coding:utf-8
import ctypes

from gorgeous.utils import *

lockfile = '/home/kali/Desktop/eoms/tmp/mdeth.lock'
ldd_file = '/home/kali/Desktop/eoms/data/linkdood/im/conf/liandoudou.conf'
serverip =  {
      "isOuter": False,
      "inner": {
        "ip": "",
        "netMask": "",
        "gateway": "",
        "dns": ""
      },
      "outer": {
        "ip": "",
        "netMask": "",
        "gateway": "",
        "dns": ""
      },
      "url": ""
    }


def extract_config(cfgfile=ldd_file) :
    if not os.path.isfile(cfgfile):
        #print(json.dumps({'status':'0','errinfo':'Not found such file or direcotry %s'%cfgfile}))
        print('Not found such file or direcotry %s'%cfgfile)
        return False

    try :
        with open(cfgfile) as f :
            ldd = json.loads(f.read())
        elogo = ldd['elogo']
        config = ldd['configAddr'].split('&')
        user = config[-2].replace('user=','')
        pwd = config[-1].replace('pwd=','')
    except :
        #print json.dumps({'status':'0','errinfo':'Configuration Error %s' %cfgfile})
        print('Configuration Error %s' %cfgfile)
        return False

    print (elogo,user,pwd)
    return (elogo,user,pwd)


def decrypt_pwd(tag,enu,enp):
    myso = ctypes.CDLL("libched.so")
    myso.EC60789803D2.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_int]
    outuser_len =  len(enu)
    outpwd_len =  len(enp)
    outuser=(ctypes.c_char * outuser_len)()
    outpwd=(ctypes.c_char * outpwd_len)()
    outuserlen = myso.EC60789803D2(tag, enu, len(enu), outuser, outuser_len)
    outpwdlen = myso.EC60789803D2(tag, enp, len(enp), outpwd, outpwd_len)
    if outpwdlen <= 0 or outpwdlen <= 0:
            pass
            #print(json.dumps({'status':'0','errinfo':'decrypt faild.'}))
            return ("","")
    return (outuser[:outuserlen], outpwd[:outpwdlen])




def md_pre_cfg(cfg="/home/kali/Desktop/eoms/data/linkdood/im/vrv/prelogin/apinfo.json"):
    pass



# 修改liandoudou配置文件
def md_cfg(url,outip,inip,ldd_cfg=ldd_file):
    url = url
    url1 = url.split(':')[0]


    # 修改liandoudou.conf
    if os.path.isfile(ldd_cfg):
        try :
            with open(ldd_cfg) as f :
                src_conf = json.loads(f.read())

            src_conf['eurl'] = url
            src_conf['inip'] = inip
            src_conf['outip'] = outip

            if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',url) :
                src_conf["domain"] = url1
            elif re.match('.*linkdood.cn.*',url) :
                src_conf["domain"] = 'linkdood.cn'
            else :
                src_conf["domain"] = url1

            with open(ldd_cfg,"w") as f :
                json.dump(src_conf,f,ensure_ascii=False,sort_keys=True,indent=4)
        except BaseException as e:
            #vlog.jprint({'status':'0','errinfo':'ldd Config Error'})
            return False
    else :
        #vlog.jprint({'status':'0','errinfo':'%s'%e})
        return False


    return True




# 简单锁 避免程序重复调用
class lockError(BaseException):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo


def lock(ctl='islock',lockfile=lockfile):
    if ctl == 'islock' :
        if os.path.isfile(lockfile):
            return True
        else :
            return False
    elif ctl == 'remove':
        os.remove(lockfile)
        return True
    elif ctl == 'create':
        f = open(lockfile,'w')
        f.close()
        return True
    else :
        return False


def manual():
    print('Example :\n    python3 %s {"isOuter":true,"inner":{"ip":"192.168.165.1","netMask":"255.255.255.0","gateway":"192.168.165.2","dns":"8.8.8.8"},"outer":{"ip":"","netMask":"","gateway":"","dns":""},"url":"vrv.linkdood.cn"}'%sys.argv[0])


# 获取网卡信息
def get_eth_info():

    eth_info = {}

    info = psutil.net_if_addrs()
    for k,v in info.items():
        # print(v)
        for item in v:
            # print(item[1])
            # if item[0] == 2 and not item[1]=='127.0.0.1':
            # print(item[1])
            if  "192" in item[1]:
                eth_info[item[1]]=k
    # print(eth_info)
    return eth_info  


# 解析liandoudou配置文件
def get_ldd_info(cfg=ldd_file):
    src_conf = {}
    try :
       with open(cfg) as f :
            src_conf = json.loads(f.read())
    except :
        pass
    
    inip = src_conf.get('inip') if src_conf else None
    outip = src_conf.get('outip') if src_conf else None
    eurl = src_conf.get('eurl') if src_conf else None
    return inip, outip, eurl


# 修改网卡
def md_net_card(eth,ips,check=False):

    eth_file = "/etc/sysconfig/network-scripts/ifcfg-%s" %eth
    if not os.path.isfile(eth_file):
        eth_file = "/etc/sysconfig/network-scripts/ifcfg-Auto_%s" %eth
        if not os.path.isfile(eth_file):
            #vlog.jprint({'status':'0','errinfo':'找不到网卡配置文件%s'%eth_file})
            return False
    
    with open(eth_file) as f :
        content = f.readlines()

    # 用来返回网卡信息 不做修改
    if check : 
        for i in content:
            if i.startswith('IPADDR=') :
                serverip['inner']['ip'] = i.lstrip('IPADDR=').rstrip('\n')
                serverip['inner']['ip'] = "192.168.10.105"
            elif i.startswith('GATEWAY=') :
                serverip['inner']['gateway'] = i.lstrip('GATEWAY=').rstrip('\n')
                serverip['inner']['gateway'] = "192.168.10.1"
            elif i.startswith('NETMASK=') :
                serverip['inner']['netMask'] = i.lstrip('NETMASK=').rstrip('\n')
                serverip['inner']['netMask'] = "255.255.255.0"
            elif i.startswith('DNS1=') :
                serverip['inner']['dns'] = i.lstrip('DNS1=').rstrip('\n')
                serverip['inner']['dns'] = "202.106.195.68"
        return True



    for k,v in ips.items():
        para =  "%s=%s\n" %(k,v)
        for line in content :
            flag = 0
            if re.match('^%s.*'%k,line):
                flag = 1
                break

        if flag :
            content[content.index(line)] = para
        else :
            content.append(para)

    content = ''.join(content)

    # 修改网卡
    #with open(eth_file,"w+") as f :
    #    f.write(content_info)
    return True


def restart_net_services():
    # 启动网卡服务
    status,eth = subprocess.getstatusoutput("/etc/init.d/network restart")

    if status :
        #vlog.jprint({'status':'0','errinfo':'启动网络服务失败'})
        return False

    return True



# 解析数据修改网卡及服务ip
def parse(args):
    try :
        args = json.loads(args)
    except BaseException as e :
        # vlog.jprint({'status':'0','errinfo':'格式错误%s'%args})
        return False

    i = args.get('inner')
    # 内网网卡系信息
    eth_in = {'IPADDR':i.get('ip'),
        'NETMASK':i.get('netMask'),
        'GATEWAY':i.get('gateway'),
        'DNS1':i.get('dns')}

    # 外网网卡信息   
    if args.get('isOuter'):
        o = args.get('outer')
        eth_out = {'IPADDR':o.get('ip'),
            'NETMASK':o.get('netMask'),
            'GATEWAY':o.get('gateway'),
            'DNS1':o.get('dns')}
    else :
        eth_out = False

    url = args.get('url')

    inip,outip,eurl = get_ldd_info() # 获取liandoudou的内网和外网ip
    eth_info = get_eth_info()   # 获取当前网卡信息对应的ip

    
    # 修改外网ip
    if eth_out :
        if eth_info.get(outip) :
            if not md_net_card(eth_info.get(outip),eth_out):
                return False
        else:
            #vlog.jprint({'status':'0','errinfo':'找不到现有的外网ip网卡信息'})
            return False

    # 修改内网ip
    if eth_info.get(inip) :
        if not  md_net_card(eth_info.get(inip),eth_in) :
            return False
    else:
        #vlog.jprint({'status':'0','errinfo':'找不到现有的内网ip网卡信息'})
        return False
    return True
    # 重启网络服务
    #if restart_net_services() :
    #    return True
    #else :
    #    return False


    inip = i.get('ip')
    if eth_out :
        outip = o.get('ip')
    else :
        outip = i.get('ip')
        
    if not md_cfg(url,outip,inip) :
        return False

    #vlog.jprint({'status':'1','errinfo':'修改成功'})
 

# 获取服务器ip地址信息
def get_server_info():
    inip, outip, eurl = get_ldd_info()
    eth_info = get_eth_info()
    if eth_info.get(inip) :
         md_net_card(eth_info.get(inip),0,check=True) 
    serverip['url'] = eurl
    serverip['inner']['ip'] = "192.168.10.105"
    serverip['inner']['gateway'] = "192.168.10.1"
    serverip['inner']['netMask'] = "255.255.255.0"
    serverip['inner']['dns'] = "202.106.195.68"
    return serverip
   


# 测试数据
if __name__ == '__main__':
    vlog = vlogger()

    try :
        if lock() :
            raise  lockError('lockfile already existed')
        else :
            lock('create')

#        test = '{"isOuter":true,"inner":{"ip":"192.168.165.1","netMask":"255.255.255.0","gateway":"192.168.165.2","dns":"8.8.8.8"},"outer":{"ip":"","netMask":"","gateway":"","dns":""},"url":"vrv.linkdood.cn"}'
#        parse(test)

        if len(sys.argv) > 1:
            parse(sys.argv[1])
        else :
            manual()

    except lockError as e :
        #vlog.jprint({'status':'0','errinfo':'%s'%e})
        sys.exit(1)

    lock('remove')
