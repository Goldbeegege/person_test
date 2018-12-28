# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 10:32
import uuid
import time
import hashlib
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

