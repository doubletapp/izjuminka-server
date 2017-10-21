from django.contrib.auth.models import User, Group
from rest_framework import serializers

from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)


from app.izjuminka.models import VKUser, ProposedNews


class VKUserSerializer(HyperlinkedModelSerializer):
    auth_token = SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.auth_token.hex

    def to_representation(self, value):
        result = super(VKUserSerializer, self).to_representation(value)
        if result.get("point"):
            result["point"] = list(value.point)
            if result["point"][0] == result["point"][1] == 0:
                result.pop("point")

        return result

    class Meta:
        model = VKUser

        fields = ('vk_id', 'vk_token', 'auth_token', 'phone', 'is_phone_confirmed',
                  'email', 'is_email_confirmed', 'point')


class ProposedNewsSerializer(ModelSerializer):
    class Meta:
        model = ProposedNews
        fields = ('id', 'owner', 'description', 'validate_status',
                  'validate_message', 'create_datetime')

