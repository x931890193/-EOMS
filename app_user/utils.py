# encoding: utf-8
"""
Create on: 2018-09-23 上午12:33
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""
import base64
# 重写 jwt载荷响应函数
from django.contrib.auth.backends import ModelBackend

# from app_user.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证的后端"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
		最终认证用户的方法
		:param request: 本次登录请求
		:param username: 本次登录用户名(手机号或者用户名)
		:param password: 本次登录用户密码
		:param kwargs: 其他参数
		:return: 如果认证成功（该用户确实是本网站的用户）返回user；反之，返回None
		"""
        # 查询出用户对象  调用上边自定义的函数
        
        user = User.objects.get(username=base64.b64decode(username))  # user的查找由自己实现
        #  验证用户名和密码  check_password(password) 继承自父类
        print(base64.b64decode(username))
        if user and user.check_password(password):
            return user
        # return None
        