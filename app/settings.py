import os
from .local_settings import DIR_TEMPLATES
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'django_crontab',
    'rest_framework',

    'app.izjuminka',
    'app.global_news',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DIR_TEMPLATES],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'app.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = "media/"

PHOTO_ROOT = "photos/"


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'app.izjuminka.authentication.DefaultBasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

CRONJOBS = [
    ('*/5 * * * *', 'app.global_news.cron.auto_rejected_news'),
    ('*/5 * * * *', 'app.global_news.cron.download_popular_news'),
]

NEWS_FEEDS = [
    "https://news.yandex.ru/world.rss", "https://news.yandex.ru/gadgets.rss",
    "https://news.yandex.ru/index.rss", "https://news.yandex.ru/internet.rss",
    "https://news.yandex.ru/society.rss", "https://news.yandex.ru/politics.rss",
    "https://news.yandex.ru/science.rss", "https://news.yandex.ru/incident.rss",
    "https://news.yandex.ru/sport.rss", "https://news.yandex.ru/religion.rss",
    "https://news.yandex.ru/business.rss",
]

EQUAL_WORDS_COUNT = 4
EQUAL_WORDS_PERCENT = 0.25

try:
    from .local_settings import *
except ImportError:
    print("Can't import local settings from local_settings.py")
