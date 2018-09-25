from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

# Create your views here.
from utils.eth_info import get_server_info
from utils.os_info import get_os_data
from utils.service_control import service_handler
from utils.time import realtime
from utils.service_info import vrvcheck
from utils.upload_info import upClientForm
from utils.user_statistics import user_count


class EntryView(View):
	"""主页面"""
	def get(self,request):
		user = request.user
		if user.is_authenticated:
			data = get_os_data()
			user_data = user_count(request)
			data.update(user_data)
			return render(request, "index.html", data)
		return render(request, "login.html")
		
class ServiceListView(View):
	@method_decorator(login_required(login_url="/"))
	def get(self, request):
		base = vrvcheck()  # 检查所有服务状态
		data = {"vrvserver": base}
		data.update(realtime())
		return render(request, "servicelist.html", data)
	
	@method_decorator(login_required(login_url="/"))
	def post(self, request):
		user = request.user
		server_name = request.POST.get("servername", None)
		server_mode = request.POST.get("servermode", None)
		server_port = request.POST.get("serverport", None)
		if None in [server_mode, server_name]:
			return JsonResponse({"status": 0})
		status = service_handler(server_name, server_mode, server_port)
		return JsonResponse({"status": status})


class SysecurityView(View):
	"""安全中心"""
	@method_decorator(login_required(login_url="/"))
	def get(self, request):
		return render(request, "sysecurity.html", realtime())

class UpclientView(View):
	"""文件功能"""
	@method_decorator(login_required(login_url="/"))
	def get(self, request):
		form = upClientForm()
		data = {'form': form}
		data.update(realtime())
		return render(request, "upclient.html", data)


class EthView(View):
	"""网络服务"""
	@method_decorator(login_required(login_url="/"))
	def get(self, request):
		return render(request, "eth.html", realtime())


@login_required(login_url="/")
def ethinfo(request, mode):
	if mode == "check":
		info = get_server_info()
		return JsonResponse({'data': {'serverIP': info}})