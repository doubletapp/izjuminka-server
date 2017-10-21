from rest_framework.viewsets import ModelViewSet
from django.contrib.gis.geos import Point

from app.izjuminka.serializers import ProposedNews, VKUser
from app.izjuminka.serializers import ProposedNewsSerializer, VKUserSerializer


class CustomModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):

        # Если существует вк-юзер - его нужно прописать как владельца
        vk_user = getattr(request.user, "vk_user", None)
        if vk_user:
            request.data.update({"owner": vk_user.vk_id})

        # Если существует точка - её нужно преобразовать в исходные тип данных
        if request.data.get("point"):
            point = Point(
                request.data["point"][0],
                request.data["point"][1]
            )
            request.data.update({"point": point})

        return super(CustomModelViewSet, self).create(request, *args, **kwargs)


class ProposedNewsViewSet(CustomModelViewSet):
    queryset = ProposedNews.objects.all()
    serializer_class = ProposedNewsSerializer


class VKUserViewSet(CustomModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer

    def create(self, request, *args, **kwargs):

        try:
            vk_user = VKUser.objects.get(
                vk_id=request.data.get("vk_id")
            )

            if getattr(request.user, "vk_user", None):
                request.data["vk_token"] = vk_user.vk_token

            self.get_object = lambda: vk_user
            return super(CustomModelViewSet, self).update(request, *args, **kwargs)

        except VKUser.DoesNotExist:
            return super(CustomModelViewSet, self).create(request, *args, **kwargs)


