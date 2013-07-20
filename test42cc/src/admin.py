# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class PersonAdmin(admin.ModelAdmin):
    pass


class HttpStoredQueriesAdmin(admin.ModelAdmin):
    list_display = ['path', 'method', 'user', 'date_with_time']


admin.site.register(Person, PersonAdmin)
admin.site.register(HttpStoredQuery, HttpStoredQueriesAdmin)