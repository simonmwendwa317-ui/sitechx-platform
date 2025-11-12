import os
from pathlib import Path
import environ
from datetime import timedelta
from kombu import Exchange, Queue

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'change-me-in-.env'),
    DJANGO_ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1', '[::1]']),
    DATABASE_URL=(str, 'postgis://simon1:Pr1vate.236@db:5432/sitechx_db'),
    REDIS_URL=(str, 'redis://redis:6379/0'),
    REDIS_CACHE_URL=(str, 'redis://redis:6379/1'),
    RABBITMQ_USER=(str, 'sitechx_rmq'),
    RABBITMQ_PASSWORD=(str, 'supersecret'),
    RABBITMQ_HOST=(str, 'rabbitmq'),
    RABBITMQ_PORT=(int, 5672),
    RABBITMQ_VHOST=(str, '/'),
    KAFKA_BROKER_URLS=(list, ['kafka:9092']),
    KAFKA_TOPIC=(str, 'sitechx'),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    ' 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'channels',
    'django_celery_results',
    'django_celery_beat',
    'django_filters',
    'corsheaders',

    'apps.authx',
    'apps.users',
    'apps.marketplace',
    'apps.geo',
    'apps.messaging',
    'apps.payments',
    'apps.analytics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'sitechx.urls'
WSGI_APPLICATION = 'sitechx.wsgi.application'
ASGI_APPLICATION = 'sitechx.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

DATABASES = {'default': env.db('DATABASE_URL')}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env('REDIS_CACHE_URL'),
    }
}
RATELIMIT_USE_CACHE = 'default'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [env('REDIS_URL')]},
    },
}

CELERY_BROKER_URL = (
    f"amqp://{env('RABBITMQ_USER')}:{env('RABBITMQ_PASSWORD')}"
    f"@{env('RABBITMQ_HOST')}:{env('RABBITMQ_PORT')}{env('RABBITMQ_VHOST')}"
)
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_ENABLE_UTC = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_TASK_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
    Queue('calls', Exchange('calls'), routing_key='calls'),
)
CELERY_TASK_DEFAULT_QUEUE = 'default'

KAFKA_BOOTSTRAP_SERVERS = env.list('KAFKA_BROKER_URLS')
KAFKA_TOPIC = env('KAFKA_TOPIC')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_BLACKLIST_BACKEND': 'rest_framework_simplejwt.token_blacklist.backends.RedisBlacklistBackend',
    'TOKEN_BLACKLIST_REDIS_URL': env('REDIS_URL'),
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
