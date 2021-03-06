"""
Django settings for day27_1 project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#ps+j(fho%d!zv!%hva!71%@^gt5bak3lx4&vt=kcl5tffk$^$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stu',
    'uauth',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.UserAuthMiddleware.AuthMiddleware',
    'utils.VisitTimesMiddleware.VisitTimes',
]

ROOT_URLCONF = 'day27_1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'day27_1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'day27_1',
        'POST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 配置静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 配置上传文件路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 没登录的跳转地址
LOGIN_URL= '/uauth/dj_login'

# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址不存在，则自动创建log文件夹
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    # version只能为一
    'version': 1,
    # True表示禁用loggers
    'disable_existing_loggers': False,

    # 1. 保存信息的格式类型定义。
    'formatters': {
        'default': {
            'format': '%(levelname)s %(funcName)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(created)s %(message)s'
        }
    },
    # 2. 处理信息的两种方式
    'handlers': {
        'stu_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M,超过5M重新备份，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 最大为5M
            'maxBytes': 5 * 1024 * 1024,
            # 文件地址
            'filename': '%s/log.txt' % LOG_PATH,
            # 按照上面的default格式保存信息
            'formatter': 'default'
        },
        'uauth_handlers': {
            'level': 'DEBUG',
            # 日志文件指定为5M,超过5M重新备份，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 最大为5M
            'maxBytes': 5 * 1024 * 1024,
            # 文件地址
            'filename': '%s/uauth_log.txt' % LOG_PATH,
            # 按照上面的default格式保存信息
            'formatter': 'simple'
        }
    },
    # 3， 用那种方法调用，产生一个接口来调用2
    'loggers': {
        'stu': {
            'handlers': ['stu_handlers'],
            'level': 'INFO'
        },
        'auth': {
            'handlers': ['uauth_handlers'],
            'level': 'INFO'
        }
    },
    # 4. 过滤器，这里不需要
    'filters': {

    }
}


# 配置restful api返回结果
REST_FRAMEWORK = {
    # 分页
    'DEFAULT_PAGINATION_CLASSES':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,

    # 设置搜索
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter'),
    # 返回结构自定义
    'DEFAULT_RENDERER_CLASSES':(
    'utils.RenderResponse.CustomJsonRenderer',
    )
}