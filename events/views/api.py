# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:32

from django.http import JsonResponse
from events import models


def lookup_user(request):
    ret = {"code": 1000,"msg":None}
    username = request.GET.get("username")
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        ret["code"] = 1001
        ret["msg"] = "用户名已存在"
    return JsonResponse(ret)