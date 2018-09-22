# _*_coding:utf-8_*_
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect, resolve_url
# 后台服务控制器
from django.views.decorators.http import require_http_methods

# 表单
from gorgeous.forms import upClientForm
from vrvtools import mdeth
from vrvtools import mdupd
from vrvtools import sshmodifi
from vrvtools.to_django import *
from vrvtools.vrvctrl import *


# 用户登录
def login(request):
	user = None
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			# request.session.set_expiry(60 * 30)  # session半个小时后过期
			# request.session.set_expiry(0)
			return HttpResponseRedirect('../')
		else:
			return render(request, 'login.html', {'login_err': '用户名或密码错误'})
	# elif request.user.is_authenticated
	else:
		return render(request, 'login.html')


# Create your views here.
# 主页
# @login_required
def index(request):
	user = request.user
	if user.is_authenticated:
		try:
			sysinfo = get_data()
			sysinfo.update(realtime())
		except BaseException:
			return render(request, 'index.html')
			# raise Http404()
		return render(request, 'index.html', sysinfo)
	else:
		return redirect("login")


# 用户中心配置
@login_required
def profile(request):
	return render(request, 'profile.html', realtime())




@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("../login")


# 服务列表展示
@login_required
def servicelist(request):
	if request.method == "POST":
		logs = request.POST.get('logname')
		logdir = request.POST.get('logdir')
		server = request.POST.get('servername')
		mode = request.POST.get('servermode')
		# print(logs, logdir, server, mode)
		# 服务启停
		if server and mode:
			vrvctrl(server, mode)
			return HttpResponse(json.dumps({'status': '1'}))
		
		# 日志下载
		if logs and logdir:
			logs = json.loads(logs)
			global logfile
			logfile = getlog(logdir, logs)
			if logfile:  # 打包完毕后下载日志
				return HttpResponse(json.dumps({'status': '1'}))
			else:  # 打包失败
				return HttpResponse(json.dumps({'status': '0'}))
		return HttpResponse(json.dumps({'status': '0'}))
	
	base = vrvcheck()  # 检查所有服务状态
	# print(base)
	data = {"vrvserver": base}
	data.update(realtime())
	return render(request, 'servicelist.html', data)


# 日志下载
@login_required
def downlog(request):
	logzip = open(logfile, 'rb')
	response = FileResponse(logzip)
	response['Content-Type'] = 'application/zip'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format("log.zip")
	return response


# ssh安全配置
@login_required
def sshctrl(request, mode):
	status = {"ssh": {"isOpen": None, "port": None}}
	
	ssh_port = sshmodifi.check()  # 检查当前端口号
	
	if request.method == "POST":
		isopen = request.POST.get('isOpen')
		port = request.POST.get('port')
		if isopen:
			if ssh_port:
				sshmodifi.modifi(int(port))  # 服务开启状态修改端口
			else:
				sshmodifi.start()  # 先启动服务并修改端口
				sshmodifi.modifi(int(port))
		else:
			sshmodifi.stop()  # 关闭服务
		
		return HttpResponse(json.dumps({'code': 1}))
	
	# 返回ssh状态
	if ssh_port:
		status["ssh"]["isOpen"] = True
		status["ssh"]["port"] = ssh_port
	else:
		status["ssh"]["isOpen"] = False
	
	return HttpResponse(json.dumps({'data': status}))


# 安全中心主页
@login_required
def sysecurity(request):
	return render(request, 'sysecurity.html', realtime())


# 网卡配置中心
@login_required
def ethctrl(request, mode):
	if mode == 'check':
		info = mdeth.get_server_info()
		print(info)
		return HttpResponse(json.dumps({'data': {'serverIP': info}}))  # 返回当前网卡信息
	elif request.method == "POST" and mode == 'commit':
		info = request.POST.get('serverIP')
		if mdeth.parse(info):  # 修改当前网卡信息
			return HttpResponse(json.dumps({'code': 1}))
		else:
			return HttpResponse(json.dumps({'code': 0}))
	else:
		raise Http404()


# 网卡配置主页
@login_required
def eth(request):
	return render(request, 'eth.html', realtime())


# 客户端上传
@login_required
def upclient(request):
	# data = {'code':1,'data':'','error'}
	if request.method == 'POST':
		form = upClientForm(request.POST, request.FILES)
		
		if form.is_valid():
			mdupd.mdupd(request.POST, request.FILES.get('files'))
			return HttpResponse('成功')
			# return HttpResponse(json.dumps({'code':1}))
		else:
			data = {'form': form}
			data.update(realtime())
			return render(request, 'upclient.html', data)
	else:
		form = upClientForm()
		data = {'form': form}
		data.update(realtime())
	return render(request, 'upclient.html', data)


# 修改密码
@login_required  # (login_url='gorgeous:login')
@require_http_methods(["GET", "POST"])
def change_password(request):
	if request.method == 'POST':
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')
		new_password2 = request.POST.get('new_password2')
		# rez = ^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_]{8,16}$
		
		if not request.user.check_password(old_password):
			changeResult = "密码错误"
		else:
			
			if new_password != new_password2:
				changeResult = "两次新密码不一致"
			else:
				if not re.match("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_]{8,16}$", new_password):
					changeResult = '密码太简单'
				else:
					# 密码字段
					request.user.set_password(new_password)
					request.user.save()
					
					# 删除登陆状态
					auth.logout(request)
					
					return redirect(resolve_url("index"))
		data =  {'context': changeResult}
		data.update(realtime())
		return render(request, 'change_password.html', data)
	
	return render(request, template_name='change_password.html', context=realtime())
	
	# return HttpResponse('OK')


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