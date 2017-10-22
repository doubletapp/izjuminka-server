from mongoengine import (
    Document, StringField, URLField, ReferenceField, IntField, DateTimeField, BooleanField, ListField,
    MapField,  EmbeddedDocumentField, EmbeddedDocument, CASCADE, CachedReferenceField, FloatField, BinaryField, DictField
)


class OldNews(Document):
    original_title = StringField()
    original_description = StringField()
    vector_words = ListField()
    created_datetime = DateTimeField()

    related_news = ListField()



