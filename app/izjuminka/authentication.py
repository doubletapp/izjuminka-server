from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from app.settings import DEFAULT_AUTHENTICATION_CREDENTIAL


class APIUser(AnonymousUser):
    def is_staff(self):
        return True


class DefaultBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        default_login = DEFAULT_AUTHENTICATION_CREDENTIAL.get("login")
        default_password = DEFAULT_AUTHENTICATION_CREDENTIAL.get("password")

        print(default_login, default_password)

        if not default_login or (userid, password) != (default_login, default_password):
            raise PermissionDenied

        return (APIUser(), None)

