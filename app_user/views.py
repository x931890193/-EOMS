import base64
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from utils.time import realtime


class CreateUserView(View):
	"""创建用户视图"""
	def post(self, request):
		data = json.loads(request.body.decode())
		csrf_token = request.COOKIES.get('csrftoken')
		username_byte = base64.b64decode(data.get("username", None))
		password_byte = base64.b64decode(data.get("password", None))
		comfirm_pass_reg_byte = base64.b64decode(data.get("comfirm_pass", None))
		if None in [username_byte, password_byte, comfirm_pass_reg_byte]:
			return  JsonResponse({"error": 402, "errmsg" : "参数不全!"})
		try:
			password = password_byte.decode().replace(re.search(csrf_token, password_byte.decode()).group(), "")
			comfirm_pass = comfirm_pass_reg_byte.decode().replace(re.search(csrf_token, comfirm_pass_reg_byte.decode()).group(), "")
			
		except:
			return JsonResponse({"errno": 403, "errmsg": "未知错误!"})
		if password != comfirm_pass:
			return JsonResponse({"errno": 403, "errmsg": "密码不一致!"})
		try:
			username = username_byte.decode().replace(re.search(csrf_token, username_byte.decode()).group(), "")
		except:
			return JsonResponse({"errno": 403, "errmsg": "未知错误!"})
		user = authenticate(username=username, password=password)
		if user:
			return JsonResponse({"errno": 403, "errmsg": "用户已存在!"})
		try:
			user = User.objects.create_user(username=username, password=password)
			user.save()
			# 添加到session
			request.session['username'] = username
			login(request, user)
			# 重定向到首页
			return JsonResponse({"errno": 201, "errmsg": "注册成功!"})
		except Exception as e:
			return JsonResponse({"errno":403, "errmsg": e})

class LoginView(View):
	"""登录视图"""
	def post(self, request):
		csrf_token = request.COOKIES.get('csrftoken')
		form_data = json.loads(request.body.decode())
		username_byte = base64.b64decode(form_data.get("username", None))
		password_byte = base64.b64decode(form_data.get("password", None))
		
		if not all([username_byte, password_byte]) and None in [username_byte, password_byte]:
			return JsonResponse({"errmsg": "用户名或者密码缺失", "errno": 400})
		else:
			username = username_byte.decode().replace(re.search(csrf_token, username_byte.decode()).group(), "")
			password = password_byte.decode().replace(re.search(csrf_token, password_byte.decode()).group(), "")
		try:
			user = authenticate(username=username, password=password)
			response = JsonResponse({"errno": 200, "errmsg": "OK"})
			response.set_cookie(base64.b64encode(("whoareyou".encode())).decode(), base64.b64encode(str(user.id).encode()))
			request.session["user_id"] = user.id
			login(request, user)  # 当前会话的对象加上属性
			return response
		except:
			return JsonResponse({"errmsg": "用户名或者密码错误", "errno": 500})
		#
	
	def get(self, request):
		return render(request, "index.html")


class UserInfoView(View):

	def get(self, request):
		user = request.user
		return render(request, "profile.html", {"time": realtime().get("time")})



class ChangePassword(View):
	
	def get(self, request):
		user = request.user
		return render(request, "change_password.html", {"time": realtime().get("time")})
	
	def post(self,request):
		
		user = request.user
		csrf_token = request.COOKIES.get('csrftoken')
		data = json.loads(request.body.decode())
		old_pass_byte = base64.b64decode(data.get("old_pass", None))
		new_pass_byte = base64.b64decode(data.get("new_pass", None))
		comfirm_pass_byte = base64.b64decode(data.get("comfirm_pass", None))
		if old_pass_byte:
			old_pass = old_pass_byte.decode().replace(re.search(csrf_token, old_pass_byte.decode()).group(), "")
			if not user.check_password(old_pass):
				return JsonResponse({"errno": 401, "errmsg": "密码错误！"})
			if None in [new_pass_byte, comfirm_pass_byte]:
				return JsonResponse({"errno": 402, "errmsg": "Not Enough Parmas!"})
			new_pass = new_pass_byte.decode().replace(re.search(csrf_token, new_pass_byte.decode()).group(), "")
			comfirm_pass = comfirm_pass_byte.decode().replace(re.search(csrf_token, comfirm_pass_byte.decode()).group(), "")
			if new_pass != comfirm_pass:
				return JsonResponse({"errno": 403, "errmsg": "Discrepancy"})
			if len(comfirm_pass) < 3:
				return JsonResponse({"errno": 402, "errmsg": "Too Simple"})
			if user.check_password(comfirm_pass):
				return JsonResponse({"errno": 200, "errmsg": "No Change"})
			try:
				user.set_password(comfirm_pass)
				return JsonResponse({"errno": 202, "errmsg": "Change Completely, Re-login"})
			except:
				return JsonResponse({"errno": 400, "errmg": "Unknown"})
		else:
			return JsonResponse({"errno": 402, "errmsg": "Not Enough Parmas!"})
		

class LogOut(View):
	
	def get(self, request):
		user = request.body
		logout(request)
		return render(request, "login.html")


