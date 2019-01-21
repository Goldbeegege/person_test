# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 10:32
import uuid
import time
import hashlib
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from events import models
"""
存放于auth相关的函数
"""

class Auth:
    def __init__(self):
        pass

    @staticmethod
    def token(username):
        uu = str(uuid.uuid4())
        times = str(time.time())
        ha = hashlib.sha1(times+uu)
        ha.update(username)

        token_value = ha.hexdigest()

        return token_value

    @staticmethod
    def encryption(password):
        pwd = list(password)
        pwd.reverse()
        pa = "0".join(password)
        ha = hashlib.sha1(pa)
        ha.update(password)
        new_pwd = ha.hexdigest()
        return new_pwd


class ViewAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method != "OPTIONS":
            ret = {"code": 2001, "error": "认证失败", "msg": "请先登陆后访问"}
            token = request.query_params.get("token","")
            if token:
                user_id = request.session.get("user_id")
                if not user_id:
                    raise AuthenticationFailed(ret)
                try:
                    user = models.UserInfo.objects.filter(id=user_id,token__token=token).first()
                    return user_id,user.username
                except Exception as e:
                    raise AuthenticationFailed(ret)
            raise AuthenticationFailed(ret)
        else:
            pass