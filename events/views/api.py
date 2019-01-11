# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:32

from django.http import JsonResponse
from events import models
from rest_framework.views import APIView
from rest_framework.response import Response
from events.auth.auth import ViewAuth
from events.serializers import event_serializers
import datetime

def lookup_user(request):
    ret = {"code": 1000,"msg":None}
    username = request.GET.get("username")
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        ret["code"] = 1001
        ret["msg"] = "用户名已存在"
    return JsonResponse(ret)


class BackUp(APIView):
    authentication_classes = [ViewAuth]
    def get(self,request,*args,**kwargs):
        #返回用户要做的事件
        backup = models.ToDo.objects.filter(user_id=request.user).all()
        ser = event_serializers.ToDoSerializer(instance=backup,many=True)
        day = datetime.datetime.now()
        record = day + datetime.timedelta(days=-1)
        obj = models.ToDo.objects.filter(user_id=request.user).extra(where=["strftime('%%Y-%%m-%%d',create_time)=%s"],params=[day.date()]).first()
        print obj

        return Response(ser.data)

class ToBedone(APIView):
    authentication_classes = [ViewAuth]
    def get(self,request,*args,**kwargs):
        today_things = models.HaveToDo.objects.filter(user_id=request.user).all()

        return Response('...')