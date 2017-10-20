from django.conf.urls import url, include
from rest_framework import routers
from app.izjuminka import views
from django.contrib import admin

from app.izjuminka.views import (
    ProposedNewsViewSet,
    VKUserViewSet
)

router = routers.DefaultRouter()
router.register(r'proposednews', ProposedNewsViewSet)
router.register(r'vkuser', VKUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
