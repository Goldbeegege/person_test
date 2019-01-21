# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from events import models

# Register your models here.


admin.site.register(models.UserInfo)
admin.site.register(models.Token)
admin.site.register(models.ToDo)
admin.site.register(models.Type)
admin.site.register(models.History)