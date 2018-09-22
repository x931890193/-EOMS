import datetime

from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Os_Info_Tmp(models.Model):
    """实时展示"""
    in_time = models.DateTimeField(auto_now_add=True, help_text="记录时间")
    os_version = models.CharField(max_length=30, null=True, help_text="系统版本")
    cpu_total = models.IntegerField(help_text="CPU个数")
    mem_total = models.CharField(max_length=30, null=True, help_text="总内存")
    updatetime = models.CharField(max_length=20, help_text="系统启动时间")
    disk_root = models.CharField(max_length=20, help_text="硬盘总量")
    disk_root_p = models.CharField(max_length=20, help_text="硬盘使用率")
    disk_root_f = models.CharField(max_length=20, help_text="硬盘可用量")
    disk_root_u = models.CharField(max_length=20, help_text="硬盘使用量")
    disk_data = models.CharField(max_length=20, help_text="外挂硬盘使用量")
    disk_data_p = models.CharField(max_length=20, help_text="外挂硬盘使用量")
    disk_data_f = models.CharField(max_length=20, help_text="外挂硬盘使用量")
    disk_data_u = models.CharField(max_length=20, help_text="外挂硬盘使用量")
    login_num = models.IntegerField(help_text="当前登录用户数")
    proc_num = models.IntegerField(help_text="进程数")
    net_conn = models.IntegerField(help_text="当前连接数")
    ssh_status = models.CharField(max_length=5, help_text="SSH状态")
    netin = models.BigIntegerField(help_text="流量下行")
    netout = models.BigIntegerField(help_text="流量上行")
    
    class Meta:
        db_table = "tb_os_info"
        verbose_name = "系统临时信息"

    def __str__(self):
        return '%s  %s  %s' % (self.os_version, self.cpu_total, self.in_time)


class OS_Info_Static(models.Model):
    """长期存储"""
    in_time = models.DateTimeField(auto_now_add=True, help_text="记录时间")
    cpu = models.FloatField(help_text="CPU1利用率")
    cpu_1 = models.FloatField(help_text="CPU2利用率")
    cpu_2 = models.FloatField(help_text="CPU3利用率")
    cpu_3 = models.FloatField(help_text="CPU4利用率")
    memory = models.IntegerField(help_text="内存")
    swap = models.IntegerField(help_text="交换空间")
    netin = models.BigIntegerField(help_text="下行流量")
    netout = models.BigIntegerField(help_text="上行流量")
    
    class Meta:
        db_table = "tb_os_static"
        verbose_name = "静态记录"
    
    def __str__(self):
        return '%s  %s  %s' % (self.in_time, self.memory, self.swap)