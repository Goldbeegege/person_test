# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 9:50

from django import forms
from events import models

class UserForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=3,
        error_messages={
            "required":"用户名不能为空",
            "max_length":"用户名长度不能超过16和字符",
            "min_length":"用户名长度不能少于3个字符",
        }
    )

    password = forms.CharField(
        max_length=16,
        min_length=8,
        error_messages={
            "required": "密码不能为空",
            "max_length": "密码长度不能超过16和字符",
            "min_length": "密码长度不能少于3个字符",
        }
    )
    re_password = forms.CharField(
        error_messages={
            "required": "请确认密码",
        }
    )

    email = forms.EmailField(
        error_messages={
            "required":"请输入邮箱",
            "invalid":"请输入正确的邮箱地址"
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = models.UserInfo.objects.filter(username=username).first()
        if user:

            self.add_error("username","用户名已存在")
        else:
            return self.cleaned_data["username"]

    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd != re_pwd:
            self.add_error("re_password","两次密码输入不一致")
        else:
            return self.cleaned_data







