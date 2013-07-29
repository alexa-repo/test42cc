# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'birth_date']


class HttpStoredQueriesAdmin(admin.ModelAdmin):
    list_filter = ['priority']
    list_display = ['path', 'method', 'user', 'date_with_time', 'priority']


class ModelsActionsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'action', 'date_with_time']


admin.site.register(Person, PersonAdmin)
admin.site.register(HttpStoredQuery, HttpStoredQueriesAdmin)
admin.site.register(ModelsActions, ModelsActionsAdmin)
