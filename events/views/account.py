# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
import copy
from events import models
from events.form_models import event_forms
from django.shortcuts import HttpResponse
from events.auth.auth import Auth
from geetest import GeetestLib
import json
from utils.exceptions import BaseResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser,FormParser
from utils.formation import StringFormation
# Create your views here.

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

class Register(APIView):
    """
    注册视图
    """

    def post(self,request,*args,**kwargs):
        ret = BaseResponse()
        data = StringFormation(request.data.keys()[0]).data
        form = event_forms.UserForm(data)
        if form.is_valid():
            #验证成功后将用户信息写入session,创建新的token
            data = copy.deepcopy(form.cleaned_data)
            del data["re_password"]
            data["password"] = Auth.encryption(data["password"])
            user = models.UserInfo.objects.create(**data)
            ret.msg = "注册成功"
            token = Auth.token(user.username)
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            ret.username = user.username
            ret.token = token
            models.Token.objects.create(user=user,token=token)
        else:
            ret.code = 1001
            ret.msg = "登录失败"
            ret.error = []
            for key,value in form.errors.items():
                ret.error.append(list(value.data[0])[0])
        return Response(ret.response_dict)


class Login(APIView):
    """
    登录视图
    """
    def get(self,request,*args,**kwargs):
        user_id = 'test'
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = gt.pre_process(user_id)
        response_str = gt.get_response_str()
        response_obj = json.loads(response_str)
        response_obj["user_id"] = user_id
        response_obj["status"] = status
        response = json.dumps(response_obj)
        return HttpResponse(response)





    def post(self,request,*args,**kwargs):
        ret = BaseResponse()
        data = StringFormation(request.data.keys()[0]).data
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = data.get(gt.FN_CHALLENGE, '')
        validate = data.get(gt.FN_VALIDATE, '')
        seccode = data.get(gt.FN_SECCODE, '')
        user_id = data.get("user_id")
        status = data.get("status")
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            username = data.get("username")
            passwrod = Auth.encryption(data.get("password"))
            user = models.UserInfo.objects.filter(username=username,password=passwrod).first()
            if user:
                token = Auth.token(user.username)
                models.Token.objects.update_or_create(user=user,defaults={"token":token})
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                ret.msg = "登录成功"
                ret.token = token
                ret.username = user.username
            else:
                ret.code = 1001
                ret.msg = "登录失败"
                ret.error = "用户名或密码错误"
        return Response(ret.response_dict)

def logout(request):
    ret = {"code":3000,"msg":None,"error":None}
    try:
        request.session.flush()
        request.COOKIES.clear()
    except Exception as e:
        ret["code"] = 3001
        ret["msg"] = "请稍后重试"
        ret["error"] = "未知错误"
    return JsonResponse(ret)