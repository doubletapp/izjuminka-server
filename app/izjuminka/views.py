import json
import vk

from urllib.parse import parse_qs, urlparse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import loader
from django.http.request import QueryDict

from .models import ProposedNews, VKUser, NewsPhoto, AdminUser
from .serializers import ProposedNewsSerializer, VKUserSerializer, AdminUserSerializer
from app.settings import MEDIA_ROOT


class AdminUserViewSet(ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer


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
    queryset = ProposedNews.objects.all()
    serializer_class = ProposedNewsSerializer

    def create(self, request, *args, **kwargs):
        photo_objects = []
        for photo in request.data.get("photos", []):
            try:
                print(photo)
                print(photo[
                    len("http://{}{}".format(get_current_site(request), MEDIA_ROOT)):
                ])
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


class AuthVK(APIView):
    template = loader.get_template('auth_vk.html')

    @staticmethod
    def get_content(request):
        user = AdminUser.objects.get(user=request.user)
        print("AdminUser", user)
        session = vk.Session(access_token=user.vk_token)
        api = vk.API(session)
        path_photo_user = api.users.get(user_ids=user.vk_id, fields='photo_200')[0]['photo_200']
        context = {
            'path_photo': path_photo_user,
            'token': user.vk_token
        }

        return context

    def get(self, request):
        print(request.method)
        template = loader.get_template('auth_vk.html')
        try:
            context = self.get_content(request)
        except AdminUser.DoesNotExist:
            context = {}

        return HttpResponse(template.render(context, request))

    def post(self, request):
        print(request.method)
        api_url = request.POST['api_url']
        query = parse_qs(urlparse('/?' + api_url).query, keep_blank_values=True)
        try:
            user = AdminUser.objects.get(user=request.user)
            user.vk_token = query['access_token'][0]
            user.save()
        except AdminUser.DoesNotExist:
            AdminUser.objects.create(user=request.user, vk_token=query['access_token'][0], vk_id=query['user_id'][0])
        context = self.get_content(request)

        template = loader.get_template('auth_vk.html')
        return HttpResponse(template.render(context, request))


class DeleteAuthVK(APIView):
    def get(self, request):
        return HttpResponsePermanentRedirect("/admin/auth_vk/")

    def post(self, request):
        print('hsdfjfdh')
        user = AdminUser.objects.get(user=request.user)
        user.delete()
        del user
        try:
            user = AdminUser.objects.get(user=request.user)
        except AdminUser.DoesNotExist:
            pass

        request.user = User.objects.get(id=request.user.id)

        return HttpResponseRedirect("/admin/")


