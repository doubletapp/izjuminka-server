from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)


from app.izjuminka.models import VKUser, ProposedNews, AdminUser


def change_point(result, value):
    if result.get("point"):
        result["point"] = list(value.point)
        if result["point"][0] == result["point"][1] == 0:
            result.pop("point")
    return result

class AdminUserSerializer():
    class Meta:
        model = AdminUser
        fields = (
            'user',
            'vk_id', 'vk_token'
        )


class VKUserSerializer(HyperlinkedModelSerializer):
    auth_token = SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.auth_token.hex

    def to_representation(self, value):
        result = super(VKUserSerializer, self).to_representation(value)
        return change_point(result, value)

    class Meta:
        model = VKUser

        fields = (
            'vk_id', 'vk_token', 'auth_token', 'phone', 'is_phone_confirmed',
            'email', 'is_email_confirmed', 'point', "city"
        )


class ProposedNewsSerializer(ModelSerializer):
    def to_representation(self, value):
        result = super(ProposedNewsSerializer, self).to_representation(value)
        return change_point(result, value)

    class Meta:
        model = ProposedNews
        fields = (
            'id', 'author', 'description', 'validate_status', 'source_post',
            'validate_message', 'create_datetime', 'point', "city", "vk_url", "cash", "photo"
        )

