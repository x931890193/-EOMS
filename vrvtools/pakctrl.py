#!/usr/bin/env python3
#coding:utf-8
#author:kk
# 程序包更新


#from gorgeous.utils import *
#from vrvtools import vrvservices

import os



# 更新文件
def update(filename,filepath):
    if not  os.path.isfile(os.path.join(filepath,filename)):
        return (0,'目录下没有此文件')
    

    #if os.isfile()
    pass


# 回滚文件
def rollback():
    pass

# 获取备份文件列表
def get_pak():
    pass




if __name__ == '__main__' :
    d = '/data/linkdood/im/IMServer/server-dbconfig'
    f = 'server-dbconfig-1.0-SNAPSHOT.jar'
    a = update(f,d)
    print(a)
