from rest_framework.viewsets import ModelViewSet
from django.contrib.gis.geos import Point

from app.izjuminka.serializers import ProposedNews, VKUser
from app.izjuminka.serializers import ProposedNewsSerializer, VKUserSerializer


class BasicAuthModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        vk_user = getattr(request.user, "vk_user", None)
        if vk_user:
            request.data.update({"owner": vk_user.vk_id})

        return super(BasicAuthModelViewSet, self).create(request, *args, **kwargs)


class ProposedNewsViewSet(BasicAuthModelViewSet):
    queryset = ProposedNews.objects.all()
    serializer_class = ProposedNewsSerializer


class VKUserViewSet(ModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get("point"):
            point = Point(
                request.data["point"][0],
                request.data["point"][1]
            )
            request.data.update({"point": point})

        return super(VKUserViewSet, self).create(request, *args, **kwargs)
