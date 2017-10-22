from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from app.izjuminka.views import (
    ProposedNewsViewSet, VKUserViewSet, UploadPhoto, NewsView, TopUsers, AuthVK, DeleteAuthVK

)

router = routers.DefaultRouter()
router.register(r'my_post', ProposedNewsViewSet)
router.register(r'auth', VKUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/auth_vk/', AuthVK.as_view()),
    url(r'^admin/delete_auth_vk/', DeleteAuthVK.as_view()),
    # url(r'^admin/send_transfer/', DeleteAuthVK.as_view()),
    url(r'^upload_image/', UploadPhoto.as_view()),
    url(r'^news/', NewsView.as_view()),
    url(r'^top_users/', TopUsers.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
              # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
