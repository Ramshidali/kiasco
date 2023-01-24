from pathlib import Path
from decouple import config, Csv


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-yod5$#2w99)r9dnj^duu5t%jwnbo*^clh&vh&=vm_7))0^_*ai'

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'versatileimagefield',
    'registration',
    'mailqueue',
    
    'el_pagination',
        
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'dashboard',
    'customers',
    'general',
    'main',
    'offers',
    'orders',
    'payments',
    'product',
    'reports',
    'users',
    'web',
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

ROOT_URLCONF = 'kiasco.urls'

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
                
                'main.context_processors.main_context',                
            ],
        },
    },
]

WSGI_APPLICATION = 'kiasco.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/app/accounts/login/'
LOGOUT_URL = '/app/accounts/logout/'
LOGIN_REDIRECT_URL = '/kiasco-super-admin/'
LOGOUT_REDIRECT_URL = '/app/accounts/login/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = (BASE_DIR / 'static'/ 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

PASSWORD_ENCRYPTION_KEY = 'a54MqS4Re_tP6nlVYX6fBBAc025sztJw6URlW35vxCY='
RZP_ID_KEY = 'rzp_live_JeBmeKCs93Z4h0'
RZP_SECRET_KEY = '9576y9uExlEQSUUj0WUkqW0z'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.in'
EMAIL_HOST_USER = 'production@kiasco.com'
EMAIL_HOST_PASSWORD = 'I88hm#AKAb4&!S-?'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'production@kiasco.com'
DEFAULT_BCC_EMAIL = 'production@kiasco.com'
DEFAULT_REPLY_TO_EMAIL = 'production@kiasco.com'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

EL_PAGINATION_PREVIOUS_LABEL = "Previous"
EL_PAGINATION_NEXT_LABEL = "Next"
EL_PAGINATION_USE_NEXT_PREVIOUS_LINKS = True
EL_PAGINATION_DEFAULT_CALLABLE_EXTREMES = 1
EL_PAGINATION_DEFAULT_CALLABLE_AROUNDS = 1
