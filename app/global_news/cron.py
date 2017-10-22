# from django.contrib.auth.models import User

from datetime import datetime
    import dateutil

def test_scheduled_job():
    print(1)

from datetime import datetime
import feedparser
from urllib.request import Request, urlopen
import copy
import pymorphy2

from pprint import pprint

morph = pymorphy2.MorphAnalyzer()


def to_word_vector(text):
    words = [morph.parse(w)[0] for w in text.split(" ")]
    result = []

    for word in words:
        if word.tag.POS in ["NOUN", "VERB", "NUMR"]:
            result.append(word.normal_form)
    return result



def download_popular_news():

    rssparse = feedparser.parse("https://news.yandex.ru/world.rss")

    from pprint import pprint
    pprint(datetime.strftime(rssparse['entries'][0]['published'], '%d %b %Y %I:%M%p'))

    data = [{
        "title": to_word_vector(obj['title']),
        "summary": to_word_vector(obj['title'])
    } for obj in rssparse['entries']]

    # rr = morph.parse(data[0]["title"])
    pprint(data)




    # print(
    #     rssparse['entries']['title']
    # )

    # last_update_datetime = rss['last_update']

    #if len(rssparse.entries) == 0:
        #logger.error("Error download "+str(rss))
    #
    # all_news = []
    #
    # for item in rssparse.entries:
    #     c_dt = item.published_parsed
    #     current_datetime = datetime(c_dt.tm_year, c_dt.tm_mon, c_dt.tm_mday, c_dt.tm_hour, c_dt.tm_min, c_dt.tm_sec)
    #
    #     if last_update_datetime is None or current_datetime > last_update_datetime:
    #         category = "Без категории"
    #         if "category" in item:
    #             category = item.category
    #
    #         req = Request(url=item.link)
    #         req.add_header('User-agent', 'Mozilla/5.0')
    #
    #         #key = ""
    #
    #         try:
    #             page = urlopen(req).read()
    #         except Exception as ex:
    #             page = ''
    #
    #         #if key != "Loading Error":
    #         #    fs = gridfs.GridFS(db)
    #         #    key = fs.put(page)
    #
    #         source = copy.deepcopy(source)
    #         source.pop("rss")
    #         source["rss"] = rss
    #
    #         news = {
    #             "source": source,
    #             "title": item.title,
    #             "category": category,
    #             "link": item.link,
    #             "datetime": current_datetime,
    #             "description": item.summary,
    #             "processed": False,
    #             "page": page,
    #         }
    #
    #         all_news.append(news)
    #
    #     return all_news


if __name__ == "__main__":
    download_popular_news()

    # print(User.objects())


    # import vk
    #
    # session = vk.AuthSession(
    #     app_id='6227710',
    #     user_login='sardnej4@yandex.ru',
    #     user_password='tunis123qwe'
    # )
    # session = vk.Session(access_token='8cdddea4b0b07f95939f89d28a53b2de54952afd94f02f0e812eb31d57faaac906f0305f368')
    # api = vk.API(session)

    #
    # print(api)
    #
    # print(api.wall.post(owner_id=444485291, message='Спасибо всем землянам'))