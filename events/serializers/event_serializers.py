# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 9:41

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from events import models

class UserSerializer(ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class HistorySerializer(ModelSerializer):
    type = serializers.CharField(source="type.title")
    completed_time = serializers.SerializerMethodField()
    def get_completed_time(self,obj):
        return obj.completed_time.strftime("%Y-%m-%d")

    class Meta:
        model = models.History
        fields = ["event_name","reason","completed_time","summary","type"]

class ToDoSerializer(ModelSerializer):
    user = serializers.CharField(source="user.username")
    type = serializers.CharField(source="type.title")
    create_time = serializers.SerializerMethodField()

    def get_create_time(self,obj):
        return obj.create_time.strftime("%Y-%m-%d")

    class Meta:
        model = models.ToDo
        fields = ["id","title","detail","create_time","user","type","is_completed","reason","summary"]

