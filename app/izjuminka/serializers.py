from django.contrib.auth.models import User, Group
from rest_framework import serializers

from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)

from app.izjuminka.models import VKUser, ProposedNews


class VKUserSerializer(HyperlinkedModelSerializer):
    auth_token = SerializerMethodField()
    point = SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.auth_token.hex


    def get_point(self, obj):
        return list(obj.point)[::-1]

    class Meta:
        model = VKUser

        fields = ('vk_id', 'vk_token', 'auth_token', 'phone', 'is_phone_confirmed',
                  'email', 'is_email_confirmed', 'point')


class ProposedNewsSerializer(ModelSerializer):
    class Meta:
        model = ProposedNews
        fields = ('owner', 'title', 'description', 'validate_status',
                  'validate_message', 'url_published_news', 'creation_data')

