from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from app.izjuminka.models import VKUser, ProposedNews


class VKUserAdmin(ModelAdmin):
    pass


class ProposedNewsAdmin(ModelAdmin):
    pass


site.register(VKUser, VKUserAdmin)
site.register(ProposedNews, ProposedNewsAdmin)
