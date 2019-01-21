# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:31

from django.conf.urls import url
from events.views import api


urlpatterns = [
    url(r'^v1/lookupUser/$',api.lookup_user),
    url(r'^v1/completion/$',api.TodayEventView.as_view({"get":"list","post":"create","delete":"distory"})),
    url(r'^v1/completion/(?P<id>\d+)/$',api.TodayEventView.as_view({"get":"retrieve"})),
    url(r'^v1/backup/$',api.BackUpEventView.as_view({"get":"list","post":"create","delete":"distory"})),
    url(r'^v1/type_list/$',api.TypeView.as_view({"get":"list","post":"create",})),
]
