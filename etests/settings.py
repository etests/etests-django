import os
import re

import dj_database_url

from datetime import timedelta
from distutils.util import strtobool
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "TOP_SECRET_KEY")

EMAIL_ID = os.getenv("NOREPLY_EMAIL_ID")

DEBUG = strtobool(os.getenv("DEBUG", "False"))

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST")]

if os.getenv("DATABASE_CONFIG", "") == "URL":
    DATABASES = {
        "default": dj_database_url.config(conn_max_age=600)
    }

elif os.getenv("DATABASE_CONFIG") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD"),
            "HOST": os.getenv("DATABASE_HOST"),
        }
    }
    
else:
     DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR , "db.sqlite3"),
        }
     }
    
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_filters",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",
    "api",
    "whitenoise.runserver_nostatic"
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

LOGIN_URL = "rest/login/"
LOGOUT_URL = "accounts/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "rest_framework_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("api.permissions.IsStaff",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
}

ROOT_URLCONF = "etests.urls"

SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "etests.wsgi.application"

AUTH_USER_MODEL = "api.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_HEADERS = (
    "Cache-Control",
    "Content-Disposition",
    "X-Requested-With",
    "Accept-Encoding",
    "Content-Type",
    "Accept",
    "Origin",
    "Authorization",
)

if os.getenv("CORS_ORIGIN_WHITELIST"):
    CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST").split(",")
else:
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

if os.getenv("DOMAIN"):
    CORS_ORIGIN_REGEX_WHITELIST = (r"^(https?://)?(\w+\.)?" + re.escape(os.getenv("DOMAIN")) + r"$",)

GEOIP_PATH = os.path.join(BASE_DIR, "GeoLite")

# Google configuration

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_APP_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_SECRET_KEY")

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    # 'social_core.pipeline.mail.mail_validation',
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# Email

EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_EMAIL_ID = os.getenv("NOREPY_EMAIL_ID")

# AWS Configuration

AWS_DEFAULT_ACL = "public-read"
AWS_REGION = "us-east-1"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

if os.getenv("AWS_S3_DOMAIN"):
    AWS_S3_DOMAIN = os.getenv("AWS_S3_DOMAIN")
else:
    AWS_S3_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_MEDIA_LOCATION = "media"
DEFAULT_FILE_STORAGE = "etests.storage_backends.MediaStorage"

AWS_STATIC_LOCATION = "static"

if os.getenv("STATIC_CONFIG", "") == "AWS":
    STATIC_URL = "https://%s/%s/" % (AWS_S3_DOMAIN, AWS_STATIC_LOCATION)
    STATICFILES_STORAGE = "etests.storage_backends.StaticStorage"

elif os.getenv("STATIC_CONFIG", "") == "WHTENOISE":
    STATIC_URL = "/static/"
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR,'media')
    MEDIA_URL = '/media/'
    
else:
    STATIC_URL = "/static/"

# Razorpay Configuration

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

try:
    from local_settings import *
except ModuleNotFoundError:
    pass
