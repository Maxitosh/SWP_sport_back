"""
Django settings for adminpage project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


SPORT_DEPARTMENT_EMAIL = "sport@innopolis.university"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv_boolean("DEBUG", False)

ALLOWED_HOSTS = ['188.130.155.115', 'helpdesk.innopolis.university']

if DEBUG:
    ALLOWED_HOSTS.append('localhost')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_adfs',
    'sport.apps.SportConfig'
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

ROOT_URLCONF = 'adminpage.urls'

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

WSGI_APPLICATION = 'adminpage.wsgi.application'

# Authentication

OAUTH_CLIENT_ID = os.getenv('oauth_appID')
OAUTH_CLIENT_SECRET = os.getenv("oauth_shared_secret")
OAUTH_AUTHORIZATION_BASEURL = os.getenv("oauth_authorization_baseURL")
OAUTH_GET_INFO_URL  = os.getenv("oauth_get_infoURL")
OAUTH_TOKEN_URL = os.getenv("oauth_tokenURL")
OAUTH_END_SESSION_URL = os.getenv("oauth_end_session_endpoint")

AUTHENTICATION_BACKENDS = (
     'django_auth_adfs.backend.AdfsAuthCodeBackend',
)

AUTH_ADFS = {
    "SERVER": "sso.university.innopolis.ru",
    "CLIENT_ID": OAUTH_CLIENT_ID,
    "CLIENT_SECRET": OAUTH_CLIENT_SECRET,
    "RELYING_PARTY_ID": OAUTH_CLIENT_ID,
    # Make sure to read the documentation about the AUDIENCE setting
    # when you configured the identifier as a URL!
    "AUDIENCE": f"microsoft:identityserver:{OAUTH_CLIENT_ID}",
    "CA_BUNDLE": True,
    "USERNAME_CLAIM": "upn",
    "CLAIM_MAPPING": {"first_name": "given_name",
                      "last_name": "family_name",
                      "email": "email"},
}

LOGIN_URL = "django_auth_adfs:login"
LOGIN_REDIRECT_URL = "/"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_SERVER"),
        "PORT": "",  # default 5432 will be set
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

if DEBUG:
    STATIC_URL = '/admin/static/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = '/static/'
