# encoding: utf-8
"""
Create on: 2018-09-25 下午12:58
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import datetime
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


@login_required(login_url="/")
def user_count(request):
    """
    用户总人数 , 当月新增的用户(月新),当日新增用户(日新)
    登录活跃人数  月活  日活  分析
    3、查询月新增人数：获取每月的1号的日期；2018-07-01
        t = time.localtime()  年= t.tm_year   月= t.tm_mon   日= 01/t.tm_mday    每月1号的日期的字符串：'%d-%02d-01' % (t.tm_year,
        t.tm_mon)
    User.create_time>每月的1日
    # 把日期字符串格式化成日期对象  datetime.strptime()
    4、查询日新增人数
    '%d-%02d-%02d' % (t.tm_year,t.tm_mon,t.tm_mday)
    5、查询活跃人数和活跃的日期
    比较的是用户的last_login的登录时间
    User.last_login>=今天的0时0分，User.last_login<昨天的0时0分
    当前日期：昨天的日期；
    :return:
    """
    total_count = 0
    mon_count = 0
    day_count = 0
    # 查总人数
    try:
        total_count = User.objects.all().count()
    except Exception as e:
        # current_app.logger.error(e)
        print("总人数都查不了!")
        return JsonResponse({"errno": 402, "errmsg": "总人数的查不了!"})
    # 当月新增的用户(月新)
    t = time.localtime()  # 时间结构体
    # time.struct_time(tm_year=2018, tm_mon=7, tm_mday=4, tm_hour=18, tm_min=47, tm_sec=20, tm_wday=2, tm_yday=185,
    # tm_isdst=0)
    # 每月一号的日期字符串   '2018-07-01'
    # str_date = "%d-%02d-01 %02d:%02d:%02d"%(t.tm_year,t.tm_mon,t.tm_hour,t.tm_min,t.tm_sec)
    # 拼接日期字符串
    str_date_start = "%d-%02d-01" % (t.tm_year, t.tm_mon)
    # 转为格式体
    rule = "%Y-%m-%d"
    pattern_date_start = datetime.datetime.strptime(str_date_start, rule)
    # print(pattern_date_start)
    try:
        mon_count = User.objects.filter(last_login__gt=pattern_date_start).count()
    except Exception as e:
        return None
    # return jsonify(errno=RET.DBERR, errmsg='查询月新人数异常')
    # 当日新增用户(日新)
    str_date_today = "%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday)
    pattern_date_today = datetime.datetime.strptime(str_date_today, rule)
    try:
        day_count = User.objects.filter(last_login__gt=pattern_date_today).count()
    except Exception as e:
        return None
    # return jsonify(errno=RET.DBERR, errmsg='查询日新人数异常')
    # 定义容器，存储活跃的人数和日期
    active_count = []
    active_time = []
    active_begin_date_str = '%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)
    active_begin_date = datetime.datetime.strptime(active_begin_date_str, '%Y-%m-%d')
    # 使用循环往前推31天，获取每天的开始日期0时0分0秒和结束日期0时0分0秒
    for x in range(0, 31):
        begin_date = active_begin_date - datetime.timedelta(days=x)
        end_date = active_begin_date - datetime.timedelta(days=(x - 1))
        
        try:
            count = User.objects.filter(last_login__gt=begin_date, last_login__lt=end_date).count()
        except Exception as e:
            return None
        # return jsonify(errno=RET.DBERR, errmsg='查询活跃人数异常')
        # 把日期对象转成日期字符串
        begin_date_str = datetime.datetime.strftime(begin_date, '%Y-%m-%d')
        active_count.append(count)
        active_time.append(begin_date_str)
    
    # 让活跃人数和日期数据反转
    active_time.reverse()
    active_count.reverse()
    # print(active_time,active_count)
    
    data = {
        'total_count':  total_count,
        'mon_count':    mon_count,
        'day_count':    day_count,
        'active_count': active_count,
        'active_time':  active_time
    }
    return data
