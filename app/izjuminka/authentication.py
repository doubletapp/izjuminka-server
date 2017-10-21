from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied

from .models import VKUser
from app.settings import DEFAULT_AUTHENTICATION_CREDENTIAL


class APIUser(AnonymousUser):
    def is_staff(self):
        return True


class APIVKUser(AnonymousUser):
    def __init__(self, vk_user):
        super(APIVKUser, self).__init__()
        self.vk_user = vk_user

    def is_vkuser(self):
        return True

    def is_staff(self):
        return False


class DefaultBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        default_login = DEFAULT_AUTHENTICATION_CREDENTIAL.get("login")
        default_password = DEFAULT_AUTHENTICATION_CREDENTIAL.get("password")

        try:
            vk_user = VKUser.objects.get(vk_id=userid, auth_token=password)
            return (APIVKUser(vk_user), None)

        except VKUser.DoesNotExist:
            if not default_login or (userid, password) != (default_login, default_password):
                raise PermissionDenied

        return (APIUser(), None)

