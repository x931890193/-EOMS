# encoding: utf-8
"""
Create on: 2018-09-22 下午9:56
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from app_entry import views

urlpatterns = [
    # 主页面
    path(r"", views.EntryView.as_view(), name="index"),
    # 服务列表
    path(r"servicelist/", login_required(views.ServiceListView.as_view(), login_url="/"), name="servicelist"),
    # 安全中心
    path("sysecurity/", login_required(views.SysecurityView.as_view(), login_url="/"), name="sysecurity"),
    # file upload
    path(r"upclient/", login_required(views.UpclientView.as_view(), login_url="/"), name="upclient"),
    # 网卡相关
    path(r"eth/", login_required(views.EthView.as_view(), login_url="/"), name="eth"),
    # 获取网卡信息
    re_path(r"eth/(check|commit)/", login_required(views.ethinfo, login_url="/"), name="ethcontrol"),
    # 日志相关
    path(r"log/", login_required(views.LogInfo.as_view(), login_url="/"), name="log"),
    # terminal
    path(r"terminal/", login_required(views.Terminal.as_view(), login_url="/"), name="terminal"),
]
