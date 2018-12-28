# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 9:41

from rest_framework.serializers import Serializer
from events import models

class UserSerializer(Serializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

