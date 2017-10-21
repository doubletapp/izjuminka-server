import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
import vk

from .models import ProposedNews, VKUser, NewsPhoto
from .serializers import ProposedNewsSerializer, VKUserSerializer
from app.settings import MEDIA_ROOT, VK_SERVICE_KEY, LENTACH_ID


class CustomModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):

        # Если существует вк-юзер - его нужно прописать как владельца
        vk_user = getattr(request.user, "vk_user", None)
        if vk_user:
            request.data.update({"author": vk_user.vk_id})

        # Если существует точка - её нужно преобразовать в исходные тип данных
        if request.data.get("point"):
            point = Point(
                request.data["point"][0],
                request.data["point"][1]
            )
            request.data.update({"point": point})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instns = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return instns, Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProposedNewsViewSet(CustomModelViewSet):
    serializer_class = ProposedNewsSerializer
    queryset = ProposedNews.objects.all().order_by('-create_datetime')

    def get_queryset(self):
        vk_user = getattr(self.request.user, "vk_user", None)
        if vk_user:
            return ProposedNews.objects.filter(author=vk_user).order_by('-create_datetime')
        else:
            return ProposedNews.objects.all().order_by('-create_datetime')

    def create(self, request, *args, **kwargs):
        photo_objects = []
        for photo in request.data.get("photos", []):
            try:

                news_photo = NewsPhoto.objects.get(
                    photo=photo[
                        len("http://{}{}".format(get_current_site(request), MEDIA_ROOT))+1:
                    ]
                )
                photo_objects.append(news_photo)
            except Exception as ex:
                import traceback
                print(traceback.format_exc())

        instns, response = super(ProposedNewsViewSet, self).create(request, *args, **kwargs)
        for photo_object in photo_objects:
            photo_object.proposed_news = instns
            photo_object.save()

        return response


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
            instns, response = super(VKUserViewSet, self).create(request, *args, **kwargs)

            return response


class UploadPhoto(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        try:
            new_photo = NewsPhoto.objects.create(photo=request.FILES['file'])
            return HttpResponse(json.dumps({
                "status": "ok",
                "url": "http://{}{}".format(get_current_site(request), new_photo.photo.url)
            }))
        except Exception as ex:
            return HttpResponseBadRequest(json.dumps({"status": "error"}))


class NewsView(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        count = int(request.GET.get('count', 10))

        session = vk.Session(access_token=VK_SERVICE_KEY)
        api = vk.API(session)
        result = api.wall.get(owner_id=LENTACH_ID, count=count, offset=offset)

        all_count = result[0]
        new_news = []

        for nws in result[1:]:
            text = nws.get("text")
            if text and text.find("#радиолентач"):
                new_nws = {
                    "text": text,
                    "photos": []
                }

                for attache in nws.get("attachments", []):
                    from pprint import pprint
                    if attache["type"] == "photo":
                        pprint(attache)
                        src_big = attache["photo"].get("src_big")
                        if src_big:
                            new_nws["photos"].append(src_big)

                new_news.append(new_nws)

        return JsonResponse({
            "offset": offset,
            "count": count,
            "all_count": all_count,
            "news": new_news
        })
