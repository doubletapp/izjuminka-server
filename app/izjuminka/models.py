from uuid import uuid4

from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField
)

from django.contrib.gis.db.models import PointField, GeoManager


ValidateStatus = (
    ('new', 0),
    ('rejected', 1),
    ('published', 2)
)


def uuid_hex():
    return uuid4().hex


class VKUser(Model):
    vk_id = IntegerField(primary_key=True)
    vk_token = CharField(max_length=200)
    phone = CharField(max_length=30, blank=True)
    is_phone_confirmed = BooleanField(default=False)
    email = TextField(blank=True)
    is_email_confirmed = BooleanField(default=False)
    auth_token = UUIDField(default=uuid4, editable=True, unique=True)

    point = PointField()
    objects = GeoManager()


class ProposedNews(Model):
    owner = ForeignKey(VKUser, on_delete=CASCADE)
    description = TextField()
    validate_status = CharField(max_length=9, choices=ValidateStatus)
    validate_message = TextField()
    url_published_news = TextField()
    creation_data = DateTimeField(auto_now_add=True)