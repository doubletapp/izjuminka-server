from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from app.izjuminka.models import VKUser


class VKUserAdmin(ModelAdmin):
    pass


site.register(VKUser, VKUserAdmin)
