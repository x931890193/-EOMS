from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns = [
	url('^$', views.index, name='index'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('change_password/', views.change_password, name='change_password'),
	path('profile/', views.profile, name='profile'),
	path('servicelist/', views.servicelist, name='servicelist'),
	path('sysecurity/', views.sysecurity, name='sysecurity'),
	re_path('sysecurity/(check|ssh)/', views.sshctrl, name='sshctrl'),
	path('servicelist/downlog/', views.downlog, name='downlog'),
	path('eth/', views.eth, name='eth'),
	re_path('eth/(check|commit)/', views.ethctrl, name='ethctrl'),
	path('upclient/', views.upclient, name='upclient'),
	re_path('upclient/', views.upclient, name='upclient'),
]
