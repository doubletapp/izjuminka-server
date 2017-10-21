DEFAULT_AUTHENTICATION_CREDENTIAL = {
    'login': 'admin',
    'password': 'password',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'izjuminka_db',
        'USER': 'izjuminka',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['31.186.100.172', '127.0.0.1']

SECRET_KEY = 'SECRET_KEY'

TOP_LIMIT = 10
LENTACH_ID = -29534144
VK_SERVICE_KEY = "5c6f2059b6677b3addd87cd5a45360"
CURRENT_DOMAIN = "http://api.izjuminka.media"
