from datetime import datetime, timedelta
import dateutil.parser
import re

import feedparser
import pymorphy2
from flask import Flask
from flask_mongoengine import MongoEngine

from app.global_news.models import OldNews
from app.izjuminka.models import ProposedNews
from app.settings import MONGODB_SETTINGS, EQUAL_WORDS_COUNT, EQUAL_WORDS_PERCENT, NEWS_FEEDS

morph = pymorphy2.MorphAnalyzer()


def build_app():
    app = Flask(__name__)
    app.debug = True
    app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
    db = MongoEngine(app)

    return app


def to_word_vector(text):
    words = [
        morph.parse(w)[0] for w in re.sub('[^a-zA-Zа-яА-я]', ' ', text).split(" ") if w and len(w) > 2
    ]
    result = []

    for word in words:
        if word.tag.POS in ["NOUN", "VERB", "NUMR", None]:
            result.append(word.normal_form)
    return result


def download_popular_news():
    build_app()

    for feed in NEWS_FEEDS:
        rssparse = feedparser.parse(feed)

        data = [{
            "original_title": obj['title'],
            "original_description": obj['summary'],
            "vector_words": list(set(to_word_vector(obj['summary'])) & set(to_word_vector(obj['title']))),
            # "vector_words": to_word_vector(obj['summary']),
            "created_datetime": dateutil.parser.parse(rssparse['entries'][0]['published']),
        } for obj in rssparse['entries']]

        for nws in data:
            try:
                old_news = OldNews.objects.get(__raw__={"original_title": nws["original_title"]})
            except OldNews.DoesNotExist:
                OldNews.objects.create(**nws)


def auto_rejected_news():
    build_app()

    for new_news in ProposedNews.objects.filter(validate_status="pending"):
        word_vector = to_word_vector(new_news.description)

        result = None
        max_count = 0
        for old_news in OldNews.objects(created_datetime__gte=datetime.utcnow()-timedelta(days=3)):
            crossing = set(word_vector) & set(old_news["vector_words"])
            if len(crossing) > max_count:
                max_count = len(crossing)
                result = old_news

        if result:
            percent = max_count/len(word_vector)
            if max_count >= EQUAL_WORDS_COUNT and percent >= EQUAL_WORDS_PERCENT:
                new_news.validate_status = 'rejected'
                new_news.validate_message = 'Копия популярной новости.'
                new_news.save()
                continue

        new_news.validate_status = 'in_progress'
        new_news.save()



if __name__ == "__main__":
    build_app()

    download_popular_news()

    auto_rejected_news()
