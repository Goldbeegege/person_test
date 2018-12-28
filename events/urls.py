# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:31

from django.conf.urls import url
from events.views import api


urlpatterns = [
    url(r'^v1/lookupUser/$',api.lookup_user),
]
