from uuid import uuid4

from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField, AutoField, ImageField, FloatField
)

from django.contrib.gis.db.models import PointField, GeoManager
from django.core import urlresolvers

from app.settings import PHOTO_ROOT, LENTACH_ID


ValidateStatus = (
    ('pending', 'pending'),
    ('rejected', 'rejected'),
    ('accepted', 'accepted'),
    ('rewarded', 'rewarded'),
)


class VKUser(Model):
    vk_id = CharField(max_length=100, primary_key=True, unique=True)
    vk_token = CharField(max_length=400)
    phone = CharField(max_length=50, blank=True)
    is_phone_confirmed = BooleanField(default=False)
    email = TextField(blank=True)
    is_email_confirmed = BooleanField(default=False)
    auth_token = UUIDField(default=uuid4, editable=True)
    create_datetime = DateTimeField(auto_now_add=True)

    city = CharField(max_length=400, null=True, blank=True, default=None)
    point = PointField(null=True, blank=True, default=None)
    objects = GeoManager()

    def __str__(self):
        return str(self.vk_id)


class ProposedNews(Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(VKUser, on_delete=CASCADE, null=True, blank=True, default=None)
    description = TextField()
    vk_id_reference = CharField(max_length=200, blank=True, default=None, null=True)
    validate_status = CharField(max_length=200, choices=ValidateStatus, default=ValidateStatus[0][1])
    validate_message = TextField(blank=True)
    cash = FloatField(default=0, blank=True)
    create_datetime = DateTimeField(auto_now_add=True)

    city = CharField(max_length=400, null=True, blank=True, default=None)
    point = PointField(null=True, blank=True, default=None)
    objects = GeoManager()

    def vk_url(self):
        if self.vk_id_reference:
            return "https://vk.com/wall{}_{}".format(LENTACH_ID, self.vk_id_reference)
        return None

    def __str__(self):
        return "{} {}".format(self.id, self.description[:40])


class NewsPhoto(Model):
    proposed_news = ForeignKey(ProposedNews, null=True, blank=True, default=None)
    photo = ImageField(blank=False, upload_to=PHOTO_ROOT)

    def __str__(self):
        return "{} {}".format(self.proposed_news.__str__(), self.photo.url)
