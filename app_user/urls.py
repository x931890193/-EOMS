# encoding: utf-8
"""
Create on: 2018-09-22 下午10:14
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from app_user import views

urlpatterns = [
    # 注册
    path(r"users/", views.CreateUserView.as_view(), name="create"),
    # path(r"users/", obtain_jwt_token),
    # 登录
    # path(r"login/", obtain_jwt_token, name="jwt_login"), # jwt 登录
    # 注册
    path(r"register/", views.CreateUserView.as_view(), name="register"),
    # 登录
    path(r"login/", views.LoginView.as_view(), name="login"),
    # 注销
    path(r"logout/", login_required(views.LogOut.as_view(), login_url="/"), name="logout"),
    # 个人中心
    path(r"userinfo/", login_required(views.UserInfoView.as_view(), "/"), name="profile"),
    # 修改密码
    path(r"changepassword/", login_required(views.ChangePassword.as_view(), login_url="/"), name="change_password")
]
