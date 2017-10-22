DEFAULT_AUTHENTICATION_CREDENTIAL = {
    'login': 'admin',
    'password': '6cceb3f9721e4baab54e95ca8cb196e1',
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

DIR_TEMPLATES = '/home/irina/irina/Project/izjuminka-server/static/templates'

TOKEN = '593d2569d9c1b57b561fe80ee4bdd7ba722aa3e7905b4ac77828a8a0efd8d375b369f0ddcc307952f6435'