from rest_framework.viewsets import ModelViewSet

from app.izjuminka.serializers import ProposedNews, VKUser
from app.izjuminka.serializers import ProposedNewsSerializer, VKUserSerializer


class ProposedNewsViewSet(ModelViewSet):
    queryset = ProposedNews.objects.all()
    serializer_class = ProposedNewsSerializer


class VKUserViewSet(ModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer
