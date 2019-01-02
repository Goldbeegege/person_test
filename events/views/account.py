# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
import copy
from events import models
from events.form_models import event_forms
from django.shortcuts import HttpResponse
from events.auth.auth import Auth
# Create your views here.

class Register(APIView):
    """
    注册视图
    """

    def post(self,request,*args,**kwargs):
        ret = {"code":1000,"msg":None}
        form = event_forms.UserForm(request.data)
        if form.is_valid():
            #验证成功后将用户信息写入session,创建新的token
            data = copy.deepcopy(form.cleaned_data)
            del data["re_password"]
            data["password"] = Auth.encryption(data["password"])
            user = models.UserInfo.objects.create(**data)
            ret["msg"] = "注册成功"
            token = Auth.token(user.username)
            request.session["user"] = user.id
            request.COOKIES["token"] = token
            models.Token.objects.create(user=user,token=token)
        else:
            ret["code"] = 1001
            for key,value in form.errors.items():
                ret[key] = list(value.data[0])[0]
        return Response(ret)


class Login(APIView):
    """
    登录视图
    """
    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        passwrod = Auth.encryption(request.data.get("password"))
        user = models.UserInfo.objects.filter(username=username,password=passwrod).first()
        ret = {"code":1000,"msg":None}
        if user:
            token = Auth.token(user.username)
            models.Token.objects.update_or_create(user=user,defaults={"token":token})
            request.session["user"] = user.id
            request.COOKIES["token"] = token
            ret["msg"] = "登录成功"
        else:
            ret["code"] = 1001
            ret["msg"] = "登录失败"
            ret["error"] = "用户名或密码错误"
        return Response(ret)

