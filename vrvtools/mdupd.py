#!/usr/bin/env python3
#
#coding:utf-8


from gorgeous.utils import *


updfile='/data/linkdood/im/conf/upd.json'

# 重启prelogin服务
def prelogin_ctr(mode='restart'):
    pre_dir = '/data/linkdood/im/vrv/prelogin/'
    cache_file = ['Save.dat','ServerUpd','UpdMap','UpdMapBeta']
    for cf in cache_file :
        f = os.path.join(pre_dir,cf)
        if os.path.isfile(f) :
            os.remove(f)
    subprocess.getstatusoutput('/usr/bin/linkd prelogin restart')

# 修改upd文件内容
def mdupd(data,client_file):
    # 上传客户端
    if not handle_client_file(client_file) :
        return False

    with open(updfile) as upd :
        updjson = json.load(upd)
    
    flag = 1
    for u in updjson :
        if u.get('deviceType') == data.get('device_type') :
            flag = 0
            u['appName'] = data.get('name')
            u['description'] = data.get('description')
            u['mark'] = data.get('mark')
            u['forceVerison'] = data.get('force_verison')
            u['version'] = data.get('version')
            u['files'][0]['fileName'] = client_file.name
            if u['files'][0].get('url') :
                u['files'][0].pop('url')
    if flag :
        new = {}
        new['appName'] = data.get('name')
        new['description'] = data.get('description')
        new['clientDefInfo'] = {}
        new['mark'] = data.get('mark')
        new['forceVerison'] = data.get('force_verison')
        new['version'] = data.get('version')
        new['files'] = [{'fileName':client_file.name}]
        updjson.append(new)

    # 写入upd.json
    with open(updfile,'w+') as wupd:
        json.dump(updjson,wupd,ensure_ascii=False,sort_keys=True,indent=4)

    prelogin_ctr()

    return True
