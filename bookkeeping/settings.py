"""
Django settings for bookkeeping project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-a&i6-ny-gfgo78#aup4pylgul3sabhm!c^6ykpk)_vizgtl027"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 第三方应用
    "rest_framework",
    "corsheaders",
    "crispy_forms",
    "crispy_bootstrap5",
    # 自定义应用
    "accounts",
    "bills",
    "stats",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # 添加CORS中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bookkeeping.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookkeeping.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# 自定义日期时间格式
DATETIME_FORMAT = "Y年n月j日 H:i"
SHORT_DATETIME_FORMAT = "Y年n月j日 H:i"
DATE_FORMAT = "Y年n月j日"
SHORT_DATE_FORMAT = "Y年n月j日"
USE_L10N = False  # 关闭本地化格式，使用我们自定义的格式


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 媒体文件设置
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Crispy Forms设置
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# REST Framework设置
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# CORS设置
CORS_ALLOW_ALL_ORIGINS = True  # 仅在开发环境中使用
CORS_ALLOW_CREDENTIALS = True

# 用户认证设置
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# 邮件发送配置
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # 使用SMTP发送邮件
EMAIL_HOST = "smtp.189.cn"  # 189邮箱的SMTP服务器
EMAIL_PORT = 465  # 使用SSL加密的端口
EMAIL_USE_SSL = True  # 使用SSL加密
EMAIL_HOST_USER = "18932667011@189.cn"  # 发件人邮箱
EMAIL_HOST_PASSWORD = "Ce@3Kj%5i%7Ai$0S"  # 邮箱授权码
DEFAULT_FROM_EMAIL = "记账软件 <18932667011@189.cn>"  # 默认发件人
EMAIL_USE_LOCALTIME = True  # 使用本地时间
EMAIL_TIMEOUT = 5  # 设置超时时间为5秒
EMAIL_SUBJECT_PREFIX = "[记账软件] "  # 邮件主题前缀

# 开发环境下不再输出到控制台
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# 密码重置设置
PASSWORD_RESET_TIMEOUT = 3600  # 密码重置链接有效期（秒）
PASSWORD_RESET_TIMEOUT_DAYS = None  # 使用秒为单位的超时设置

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
