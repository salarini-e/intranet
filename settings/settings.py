import os
from pathlib import Path
from . import envvars
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

env_vars = envvars.load_envars(BASE_DIR)

db_name = env_vars['db_name']
db_user = env_vars['db_user']
db_host = env_vars['db_host']
db_port = env_vars['db_port']
db_passwd = env_vars['db_pw']
SECRET_KEY = env_vars['django_secret_key']
debug_mode = env_vars['debug_mode']
email_user = env_vars['email_sistema']
email_pass = env_vars['email_pw']
sqlite_mode = env_vars['sqlite_mode']

DEBUG = debug_mode

ALLOWED_HOSTS = ['*']

try:
    hCAPTCHA_PUBLIC_KEY = env_vars['hCAPTCHA_Public_Key']
    hCAPTCHA_PRIVATE_KEY = env_vars['hCAPTCHA_Secret_Key']
except:
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''

try:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_vars['GOOGLE_OAUTH2_PUBLIC_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_vars['GOOGLE_OAUTH2_SECRET_KEY']

    SOCIAL_AUTH_FACEBOOK_KEY = env_vars['FACEBOOK_DEVELOPER_PUBLIC_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = env_vars['FACEBOOK_DEVELOPER_SECRET_KEY']
except:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

    SOCIAL_AUTH_FACEBOOK_KEY = ''
    SOCIAL_AUTH_FACEBOOK_SECRET = ''

el_api_token = env_vars['el_api_token']
el_id_client = env_vars['el_id_client']

INSTALLED_APPS = [
    #terceiros
    'fontawesomefree',    
    'django_select2',
    "bootstrap5",
    #default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #custom
    'autenticacao',
    'core',
    'instituicoes',
    'telefonia',
    'formfacil',
    'softwares',
    'chamados',
    'base_conhecimento',
    'agricultura_codigobarras',
    'notificacoes',
    'dashboards',
    'noticias',
    'projetos',
    'controle_de_ponto',
    'planejamento_de_acoes',
    # 'django_logwatcher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'instituicoes.middleware.ServidorMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'settings.wsgi.application'
ASGI_APPLICATION = 'settings.asgi.application'

if sqlite_mode:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_ROOT, 'yourdatabasename.db'),
        }    
    }
else:
    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.mysql',

                'NAME': db_name,
                'PORT': db_port,

                'USER': db_user,
                'PASSWORD': db_passwd,
                'HOST': db_host,
            }
    }

CACHES = {    
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SELECT2_CACHE_BACKEND = "default"

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'static/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'settings/media')


LOGIN_URL='/login'
# LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'Intranet - Nova Friburgo <turismo@sme.novafriburgo.rj.gov.br>'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = email_user
EMAIL_HOST_PASSWORD = email_pass

X_FRAME_OPTIONS = 'SAMEORIGIN'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
