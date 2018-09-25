# encoding: utf-8
"""
Create on: 2018-09-24 上午2:35
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import datetime


def realtime():
	# 时间
	now = datetime.datetime.now()
	A = now.strftime('%A')
	Y = now.strftime('%Y')
	m = now.strftime('%m')
	d = now.strftime('%d')
	H_M = now.strftime('%H:%M')
	
	data = {"time": {"A": A, "Y": Y, "m": m, "d": d, "H_M": H_M}}
	return data