# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:32

from django.http import JsonResponse
from events import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from events.auth.auth import ViewAuth
from events.serializers import event_serializers
import datetime
from utils.exceptions import BaseResponse
from utils.formation import StringFormation
BASEEXC = BaseResponse()

def lookup_user(request):
    username = request.GET.get("username")
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        BASEEXC.code = 1001
        BASEEXC.msg = "用户名已存在"
    return JsonResponse(BASEEXC.response_dict)


class TodayEventView(ViewSetMixin,APIView):
    """
    获取用户今日要做的事，即应该查询出昨日备注且未完成的事件
    """
    authentication_classes = [ViewAuth]

    def list(self,request,*args,**kwargs):
        #返回用户要做的事件
        day = datetime.datetime.now()
        record = day + datetime.timedelta(days=-1)
        backup = models.ToDo.objects.filter(user_id=request.user).extra(where=["strftime('%%Y-%%m-%%d',create_time)=%s"],params=[record.date()]).all()
        ser = event_serializers.ToDoSerializer(instance=backup, many=True)
        return Response(ser.data)

    def retrieve(self,request,*args,**kwargs):
        view_id = kwargs.get("id")
        try:
            backup = models.ToDo.objects.filter(user_id=request.user,id=view_id).first()
            ser = event_serializers.ToDoSerializer(instance=backup)
        except Exception as e:
            BASEEXC.code = 1001
            BASEEXC.msg = "请稍后尝试"
            BASEEXC.msg = "未知错误"
            ser = ""
            ser.data = ""
        return Response(ser.data)

    def create(self,request,*args,**kwargs):
        data = StringFormation(request.data.keys()[0]).data
        data_dict = {
            "event_name":data.get("title"),
            "reason":data.get("uncompleted_reason"),
            "completed_time":datetime.datetime.utcnow(),
            "summary":data.get("summary"),
            "is_completed":0 if data.get("is_completed") else 1,
            "user_id":request.user,
            "type":data.get("type")
        }
        try:
            models.History.objects.create(**data_dict)
            models.ToDo.objects.filter(id=data.get("id")).delete()
            BASEEXC.msg = "创建成功"
        except Exception as e:
            print e
            BASEEXC.code = 1001
            BASEEXC.msg = "事件信息创建失败"
            BASEEXC.error = "创建失败"

        return Response(BASEEXC.response_dict)

    def distory(self,request,*agrs,**kwargs):
        id_list = request.data.get("index_list")
        try:
            for nid in id_list:
                models.ToDo.objects.filter(id=nid).delete()
            BASEEXC.msg = "删除成功"
        except Exception as e:
            BASEEXC.code = 1001
            BASEEXC.msg = "删除失败"
            BASEEXC.error = "未知错误"
        return Response(BASEEXC.response_dict)


class BackUpEventView(ViewSetMixin,APIView):
    authentication_classes = [ViewAuth]

    """
    备注用户明日要做事件，即获取今日备注的所有事件
    """

    def list(self,request,*args,**kwargs):
        events = models.ToDo.objects.filter(user_id=request.user).all()
        ser = event_serializers.ToDoSerializer(instance=events,many=True)
        return Response(ser.data)

    def create(self,request,*args,**kwargs):
        data = request.data
        data["user_id"] = request.user
        try:
            models.ToDo.objects.create(**data)
            BASEEXC.msg = "创建成功"
        except Exception as e:
            BASEEXC.code = 1001
            BASEEXC.error = e
            BASEEXC.msg = "创建失败"
        return Response(BASEEXC.response_dict)

    def distory(self, request, *args, **kwargs):
        try:
            nid = request.data.get("id")
            models.ToDo.objects.filter(id=nid).delete()
            BASEEXC.msg = "删除成功"
        except Exception as e:
            BASEEXC.code = 1001
            BASEEXC.msg = "删除失败"
            BASEEXC.error = e
        return Response(BASEEXC.response_dict)

class History(ViewSetMixin, APIView):
    authentication_classes = [ViewAuth]

    """
    查询用户的历史记录，根据参数finish与unfinish来区分是否完成
    """

    def list(self, request, *args, **kwargs):
        is_completed = request.query_params.get("is_completed")
        history = models.History.objects.filter(user_id=request.user,is_completed=is_completed).all()
        ser = event_serializers.HistorySerializer(instance=history, many=True)
        return Response(ser.data)


class TypeView(ViewSetMixin,APIView):
    """
    查询所有事件类型，增加用户体验
    """
    authentication_classes = [ViewAuth]
    def list(self,request,*args,**kwargs):
        title_list = list(models.Type.objects.values("id","title"))
        return JsonResponse(title_list,safe=False)

    def create(self,request,*args,**kwargs):
        title = request.data.get("title")
        try:
            type_obj = models.Type.objects.create(title=title)
            BASEEXC.msg = "创建成功"
            BASEEXC.new_type = {"id":type_obj.id,"title":title}
        except Exception as e:
            BASEEXC.code = 1001
            BASEEXC.msg = "创建失败"
            BASEEXC.error = e
        return Response(BASEEXC.response_dict)
