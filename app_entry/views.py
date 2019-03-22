import subprocess

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.
from utils.eth_info import get_server_info
from utils.os_info import get_os_data
from utils.service_control import service_handler
from utils.service_info import vrvcheck
from utils.time import realtime
from utils.upload_info import upClientForm
from utils.user_statistics import user_count


class EntryView(View):
    """主页面"""
    
    def get(self, request):
        # a = request.REQUEST
        # print(a)
       # user = request.user
       # if True or user.is_authenticated:
        if True:
            data = get_os_data()
            # user_data = user_count(request)
            # data.update(user_data)
            return render(request, "index.html", data)
        return render(request, "login.html")


class ServiceListView(View):
    
    def get(self, request):
        base = vrvcheck()  # 检查所有服务状态
        data = {"vrvserver": base}
        data.update(realtime())
        return render(request, "servicelist.html", data)
    
    def post(self, request):
        user = request.user
        if user.is_superuser:
            server_name = request.POST.get("servername", None)
            server_mode = request.POST.get("servermode", None)
            server_port = request.POST.get("serverport", None)
            if None in [server_mode, server_name]:
                return JsonResponse({"status": 0})
            status = service_handler(server_name, server_mode, server_port)
            return JsonResponse({"status": status})
        else:
            return JsonResponse({"status": 2, "errmsg": "Premission Denied"})


class SysecurityView(View):
    """安全中心"""
    
    def get(self, request):
        return render(request, "sysecurity.html", realtime())


class UpclientView(View):
    """文件功能"""
    
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


class LogInfo(View):
    def get(self, request):
        return JsonResponse({'msg':'this is log'})


def ethinfo(request, mode):
    if mode == "check":
        info = get_server_info()
        return JsonResponse({'data': {'serverIP': info}})


class Terminal(View):
    
    def get(self, request):
        result, output = subprocess.getstatusoutput("/bin/ss -tnl | /usr/bin/awk '$4~/.*:8888/{print $4}'")
        data = realtime()
        if output:
            pass
        else:
            subprocess.getstatusoutput("python ./webssh/main.py")
        return render(request, "terminal.html", data)
