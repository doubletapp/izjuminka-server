from uuid import uuid4

from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField, AutoField
)

from django.contrib.gis.db.models import PointField, GeoManager


ValidateStatus = (
    ('new', 'new'),
    ('rejected', 'rejected'),
    ('published', 'published')
)


class VKUser(Model):
    vk_id = CharField(max_length=100, primary_key=True)
    vk_token = CharField(max_length=400)
    phone = CharField(max_length=50, blank=True)
    is_phone_confirmed = BooleanField(default=False)
    email = TextField(blank=True)
    is_email_confirmed = BooleanField(default=False)
    auth_token = UUIDField(default=uuid4, editable=True, unique=True)
    create_datetime = DateTimeField(auto_now_add=True)

    point = PointField(null=True, blank=True, default=None)
    objects = GeoManager()

    def __str__(self):
        return str(self.vk_id)


class ProposedNews(Model):
    id = AutoField(primary_key=True)
    owner = ForeignKey(VKUser, on_delete=CASCADE, null=True, blank=True, default=None)
    description = TextField()
    validate_status = CharField(max_length=200, choices=ValidateStatus, default=ValidateStatus[0][1])
    validate_message = TextField(blank=True)
    create_datetime = DateTimeField(auto_now_add=True)
