from django.contrib.admin import site, ModelAdmin
from app.izjuminka.models import VKUser, ProposedNews, NewsPhoto


class VKUserAdmin(ModelAdmin):
    pass


class ProposedNewsAdmin(ModelAdmin):
    pass


class NewsPhotoAdmin(ModelAdmin):
    pass


site.register(VKUser, VKUserAdmin)
site.register(ProposedNews, ProposedNewsAdmin)
site.register(NewsPhoto, NewsPhotoAdmin)
