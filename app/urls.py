from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from app.izjuminka.views import (
    ProposedNewsViewSet, VKUserViewSet, UploadPhoto, NewsView

)

router = routers.DefaultRouter()
router.register(r'my_post', ProposedNewsViewSet)
router.register(r'auth', VKUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_image/', UploadPhoto.as_view()),
    url(r'^news/', NewsView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
