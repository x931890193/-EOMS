# encoding: utf-8
"""
Create on: 2018-09-22 下午9:56
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
from django.urls import path, re_path

from app_entry import views

urlpatterns = [
	# 主页面
	path(r"", views.EntryView.as_view(), name= "index"),
	# 服务列表
	path(r"servicelist/", views.ServiceListView.as_view(), name= "servicelist"),
	# 安全中心
	path("sysecurity/", views.SysecurityView.as_view(), name="sysecurity"),
	# file upload
	path(r"upclient/", views.UpclientView.as_view(), name="upclient"),
	# 网卡相关
	path(r"eth/", views.EthView.as_view(), name="eth"),
	# 获取网卡信息
	re_path(r"eth/(check|commit)/", views.ethinfo, name="ethcontrol")
]