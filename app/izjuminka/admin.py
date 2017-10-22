from django.contrib.admin import site, ModelAdmin
from app.izjuminka.models import VKUser, ProposedNews, NewsPhoto, AdminUser, Account


class AccountAdmin(ModelAdmin):
    pass


class VKUserAdmin(ModelAdmin):
    pass

class AdminUserAdmin(ModelAdmin):
    pass


class ProposedNewsAdmin(ModelAdmin):
    list_filter = ('validate_status',)
    readonly_fields = ('vk_id_reference', 'cash', 'city', 'point')
    # raw_id_fields = ('author',)
    list_display = ('description', 'author', 'vk_id_reference', 'validate_status', 'validate_message',
                    'cash', 'create_datetime',)




class NewsPhotoAdmin(ModelAdmin):
    pass


site.register(Account, AccountAdmin)
site.register(VKUser, VKUserAdmin)
site.register(AdminUser, AdminUserAdmin)
site.register(ProposedNews, ProposedNewsAdmin)
site.register(NewsPhoto, NewsPhotoAdmin)
