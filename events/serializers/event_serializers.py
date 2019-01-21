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

class ToDoSerializer(ModelSerializer):
    user = serializers.CharField(source="user.username")
    type = serializers.CharField(source="type.title")
    create_time = serializers.SerializerMethodField()

    def get_create_time(self,obj):
        return obj.create_time.strftime("%Y-%m-%d")

    class Meta:
        model = models.ToDo
        fields = ["id","title","detail","create_time","user","type","is_completed","reason","summary"]

