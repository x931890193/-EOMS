#_*_coding:utf-8_*_
from django.contrib.auth import authenticate

__author__ = 'eoms'

import os,sys,time,re,json,subprocess,random,datetime
import psutil
import logging
from eoms.settings import *



def set_log(level, filename=LOG_FILE):
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}

    logger_f = logging.getLogger()
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f

# 日志记录器
logger = set_log(LOG_LEVEL)



# 上传的文件
def handle_uploaded_file(filename,filetype=0,filedir=False):
    '''
    filetype
        0:普通文件
        1:客户端文件
        2:程序包文件 需要指定文件路径filedir
    '''
    if filetype == 0 :
        today=time.strftime('%Y%m%d')
        uploadir = os.path.join(UPLOADED_DIR,today)
    elif filetype == 1 :
        uploadir = CLIENT_DIR
    elif filetype == 2 :
        if filedir :
            uploadir = filedir
        else :
            logger.error('没有指定filedir')
            return False

    if not os.path.isdir(uploadir) :
        os.makedirs(uploadir)

    log_file = os.path.join(uploadir,f.name)
    with open(log_file,'wb+') as dest :
        for chunk in f.chunks():
            dest.write(chunk)
    logger.info('上传文件%s到%s'%(f.name,CLIENT_DIR))
    return True

# 修改密码
def db_change_password(password,newPassword,oldpassword1,):
    user = authenticate(password=password, oldpassword1=oldpassword1)
    if user is not None:
        if user.is_active:
            user.set_password(newPassword)
            user.save()
            # print('-----------------')
            return  1   # 修改成功，允许特殊符号
        else:
            return -2   # 没有权限
    else:
        return -1   # 旧密码错误
    