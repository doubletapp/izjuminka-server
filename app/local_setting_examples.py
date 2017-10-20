DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'izjuminka_db',
        'USER': 'izjuminka',
        'PASSWORD': 'izjuminka123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['31.186.100.172', '127.0.0.1', 'izjuminka.doubletapp.ru']

SECRET_KEY = 'zvs@fbu!sla$#&$2lavt0(t8s%#9cv)1s$*_71xyv&%_&iv-og'