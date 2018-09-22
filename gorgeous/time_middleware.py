# encoding: utf-8
"""
Create on: 2018-09-22 下午6:09
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import os


def my_middelwares(get_response):
	"""for test """
	def time_middlewares(request):
		request.session["python"] = os.name
		response = get_response(request)
		# print(response)
		response.set_cookie("whoisyourdaddy", "hello world", max_age=3600)

		# response.set_cookie('itcast2', 'python2', max_age=3600)  # 有效期一小时
		return response
	return time_middlewares
