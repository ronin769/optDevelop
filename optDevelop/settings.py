"""
Django settings for optDevelop project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mlsv0m^!e=6f=0duc=)(kpw&$g(xk8ow(q&kvjj08farhhjrg6'

# SECURITY WARNING: don't run with debug turned on in production!


# Django设置 DEBUG=False后静态文件无法加载解决
# 两种配置

# DEBUG = False
# STATIC_ROOT = 'static' ## 新增行
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, '/static/'), ##修改地方
# ]

# 然后CMD下运行如下面命令，进行样式采集：
# python manage.py collectstatic





DEBUG = True
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]







USE_TZ = True

ALLOWED_HOSTS = ['*']

APPEND_SLASH = False
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'VulnManage.apps.VulnManageConfig',
    'MitmProxy.apps.MitmproxyConfig',
    'FireWall.apps.FirewallConfig',
    'RBAC.apps.RbacConfig',
    'Assets.apps.AssetsConfig',
    'PenetrationTest.apps.PenetrationtestConfig',
    'rest_framework',
    # 'rest_framework_mongoengine',
    'django_filters',
    'rest_framework.authtoken',
    'NewFireWall.apps.NewfirewallConfig',
    'Copartnership.apps.CopartnershipConfig',
    'ProjectName.apps.ProjectnameConfig',
    'HostVuln.apps.HostvulnConfig'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optDevelop.urls'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',

    ]
    # ,'DEFAULT_PERMISSION_CLASSES': [
    #     # AllowAny 允许所有用户
    #     # IsAuthenticated 仅通过认证的用户
    #     # IsAdminUser 仅管理员用户
    #     # IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取
    #
    #     # 'rest_framework.permissions.DjangoModelPermissionsOrAnon|ReadOnly',
    #     'rest_framework.permissions.IsAdminUser',
    #     'rest_framework.pagination.CursorPagination',
    #     'rest_framework.authentication.BasicAuthentication',   # 基本认证
    #     'rest_framework.authentication.SessionAuthentication',  # session认证
    #     # 'rest_framework.permissions.IsAuthenticated',
    #     'rest_framework.permissions.AllowAny',
    # ]
    ,'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': [
        'rest_framework.pagination.LimitOffsetPagination',
    ]
    # 配置过滤器
    ,'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]

}



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'optDevelop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'optmanager',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            # 'NAME': 'auto_tests1',
            'CHARSET': 'utf8',
        },
        'TEST_COLLATION': 'utf8_general_ci',
    },
    'optmongodb': {
        'ENGINE': None,
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# 图片目录必须跟 STATIC_URL 一致


STATIC_URL = '/static/'
MEDIA_DIR = BASE_DIR + "/static/media"
UPLOAD_DIR = BASE_DIR + "/static/upload"


TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}


# session保存策略（时间）
# SESSION_COOKIE_AGE = 60*60   # 30分钟
# 会话cookie可以在用户浏览器中保持有效期。True：关闭浏览器，则Cookie失效。
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

