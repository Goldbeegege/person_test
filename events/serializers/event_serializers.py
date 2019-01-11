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
    class Meta:
        model = models.ToDo
        fields = ["id","title","detail","create_time","user","type"]


class HaveToDoSerializer(ModelSerializer):
    # user = serializers.CharField(source="user.username")
    # type = serializers.CharField(source="type.title")
    class Meta:
        model = models.HaveToDo
        fields = "__all__"
