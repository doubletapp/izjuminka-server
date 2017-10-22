import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template import loader
from django.http.request import QueryDict
import vk

from .models import ProposedNews, VKUser, NewsPhoto, AdminUser
from .serializers import ProposedNewsSerializer, VKUserSerializer, AdminUserSerializer
from app.settings import MEDIA_ROOT
from .models import ProposedNews, VKUser, NewsPhoto
from .serializers import ProposedNewsSerializer, VKUserSerializer
from app.settings import MEDIA_ROOT, VK_SERVICE_KEY, LENTACH_ID, TOP_LIMIT


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




class NewsView(APIView):
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
                    "post_id": nws.get("id"),
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


class TopUsers(APIView):
    def get(self, request):
        session = vk.Session(access_token=request.user.vk_user.vk_token)
        api = vk.API(session)

        fresh_news = ProposedNews.objects.filter(
            create_datetime__gt=datetime.utcnow() - timedelta(days=7),
            validate_status__in=['accepted', 'rewarded']
        )

        users = defaultdict(lambda: defaultdict(int))

        for news in fresh_news:
            post = api.wall.get(
                posts="{}_{}".format(LENTACH_ID, news.vk_id_reference),
                owner_id=LENTACH_ID,
            )

            users[news.author.vk_id]["hyip"] += (
                post[1]["likes"]["count"] + post[1]["reposts"]["count"]
                + post[1]["comments"]["count"]
            )

        list_users = []
        you = {}

        for user, value in users.items():
            res = dict(value)
            res.update({"user": user, "is_you": False})
            if user == request.user.vk_user.vk_id:
                res["is_you"] = True
                you = res

            list_users.append(res)

        list_users = sorted(list_users, key=lambda x: -x["hyip"])

        top_users = []
        count_top_users = 0


        for i in range(len(list_users)):
            list_users[i]["position"] = i + 1
            if count_top_users < TOP_LIMIT:
                top_users.append(list_users[i])
                count_top_users += 1
            elif bool(you) is False:
                break
            elif you["user"] == list_users[i]["user"]:
                top_users.append(list_users[i])
                break

        for i in range(len(top_users)):
            try:
                user = api.users.get(user_ids=top_users[i]["user"], fields="photo_200")
                top_users[i].update({
                    'first_name': user[0]['first_name'],
                    'last_name': user[0]['last_name'],
                    'photo': user[0]['photo_200'],
                })

            except Exception as ex:
                pass

        return JsonResponse({
            "top_users": top_users,

        })