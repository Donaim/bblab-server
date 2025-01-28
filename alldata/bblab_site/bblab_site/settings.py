"""
Django settings for bblab_site project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.core.management.utils import get_random_secret_key

SITE_ID = 9

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('BBLAB_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('BBLAB_DEBUG', 'N').lower() in ['y', '1', 'true', 't']

ALLOWED_HOSTS = [
    os.environ['BBLAB_WEB_ADDRESS'],
]

if 'BBLAB_ALT_WEB_ADDRESS' in os.environ:
    ALLOWED_HOSTS.append(os.environ['BBLAB_ALT_WEB_ADDRESS'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Wiki additions
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    #'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    #'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
    'wiki.plugins.links.apps.LinksConfig',
    'wiki.plugins.help.apps.HelpConfig',

    # Brute force attack protection
    'axes',
    # 'tools.blind_dating',
    # 'tools.phylodating',
    'phylodating',
    # 'tools.phylodating.models',
    # 'tools.phylodating.apps.PhylodatingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'axes.middleware.AxesMiddleware',  # Should be last or around last.
]

CSRF_TRUSTED_ORIGINS = [
    'https://' + os.environ['BBLAB_WEB_ADDRESS'],
]

ROOT_URLCONF = 'bblab_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.environ.get('BBLAB_TEMPLATE_ROOT', 'fail'),
        os.environ.get('BBLAB_TOOL_ROOT', 'fail')
    ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

        # Django-wiki additions.
        'django.template.context_processors.i18n',
                'django.template.context_processors.media',
        'django.template.context_processors.static',
                'django.template.context_processors.tz',
        "sekizai.context_processors.sekizai",
        ],
        },
    },
]

WSGI_APPLICATION = 'bblab_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['BBLAB_DB_NAME'],
        'USER': os.environ['BBLAB_DB_USER'],
        'PASSWORD': os.environ['BBLAB_DB_PASSWORD'],
        'HOST': os.environ['BBLAB_DB_HOST'],
        'PORT': ''
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

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # For brute force protection
    'django.contrib.auth.backends.ModelBackend',  # Default model
]

# Brute force protection config
AXES_COOLOFF_TIME = None
AXES_FAILURE_LIMIT = 20
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_URL = "/django/account/lockout/"
AXES_USE_USER_AGENT = True


# Wiki config
WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False

LOGIN_URL = '/django/account/login/'
LOGOUT_URL = '/django/account/logout/'


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Etc/GMT+7'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('BBLAB_STATIC_ROOT', 'fail')

# This is for user uploaded files (CAUTION!!)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('BBLAB_MEDIA_ROOT', 'fail')

# Quick-start development settings - unsuitable for production - done!
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# Deploy Settings (for extra security, etc...)

# Only https requests must be accepted (yup)
is_true_string = lambda s : s.lower() in ('true', 't', 'y', 'yes', '1')
CSRF_COOKIE_SECURE = is_true_string(os.environ.get('BBLAB_CSRF_COOKIE_SECURE', "True"))
SESSION_COOKIE_SECURE = is_true_string(os.environ.get('BBLAB_SESSION_COOKIE_SECURE', "True"))

# When a database connection is finished it is closed immediately.
# If n != 0, the connection will be left open for some time.
# We don't have many users so we don't need the database to stay open.
CONN_MAX_AGE = 0


# This should write errors to an error log.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': '{asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.environ.get('BBLAB_LOG_FILE', ''),
            'formatter': 'main',
        },
    },
    'loggers': {
        'django': {
        	'handlers': ['logfile'],
        	'level': 'ERROR',
        	'propagate': True,
        },
    },
    'root': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        }
}

# Additional Security Settings
SECURE_CONTENT_TYPE_NOSNIFF = False  # This is the default & I think is ok.
SECURE_BROWSER_XSS_FILTER = True  # This is not the default but I think its ok.

X_FRAME_OPTIONS = 'DENY'  # This setting blocks any other part of this site from being displayed inside itself.

DATING_OUT = 'dating_out'
