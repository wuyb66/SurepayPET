"""
Django settings for SurepayPET project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import os.path
from django.utils import six

# if six.PY2 and sys.getdefaultencoding()=='ascii':
#     import imp
#     imp.reload(sys)
#
#     sys.setdefaultencoding('utf-8')

from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), os.pardir)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's4_#h_03yhyu094%0g@l=j4fq!8y%3h%flv2(d(s3m7^$qs)su'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'material.theme.lightblue',
    # 'material',
    # 'material.frontend',
    # 'material.admin',
     'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'xadmin',
    'crispy_forms',
    # 'reversion',

    # 'ajax_select',
    # 'ajax_select_cascade',

    'smart_selects',
    'clever_selects',

    'hardware.apps.HardwareConfig',
    'service.apps.ServiceConfig',
    'project.apps.ProjectConfig',
    'common.apps.CommonConfig',
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

ROOT_URLCONF = 'SurepayPET.urls'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            # 'propagate': True,
        }
    }
}

SUIT_CONFIG = {
    'MENU': (

        # Keep original label and models
        'sites',

        # Rename app and set icon
        {'app': 'auth', 'label': 'Authorization', 'icon':'icon-lock'},

        # Reorder app models
        {'app': 'auth', 'models': ('user', 'group')},

        {'app': 'common', 'label': 'Common', 'models': (
            {'model': 'GlobalConfiguration', 'label': 'Global Configuration'},
            {'model': 'DBMode', 'label': 'Database Mode'},
            {'model': 'NetworkInfo', 'label': 'Network Information'},
        ),},

        {'app': 'hardware', 'label': 'Hardware', 'models': (
            {'model': 'VMType', 'label': 'VM Type'},
            {'model': 'CPU', 'label': 'CPU'},
            {'model': 'HardwareType', 'label': 'Hardware Type'},
            {'model': 'HardwareModel', 'label': 'Hardware Model'},
            {'model': 'CPUList', 'label': 'CPU List'},
            {'model': 'MemoryList', 'label': 'Memory List'},
            {'model': 'CPUTuning', 'label': 'CPU Tuning'},
            {'model': 'MemoryUsageTuning', 'label': 'Memory Usage Tuning'},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
        ),},

        {'app': 'service', 'label': 'Service', 'models': (
            {'model': 'Release', 'label': 'Release'},
            {'model': 'CurrentRelease', 'label': 'Current Release'},
            {'model': 'ApplicationName', 'label': 'Application Name'},
            {'model': 'ApplicationInformation', 'label': 'Application Information'},
            {'model': 'OtherApplicationInformation', 'label': 'Other Application Information'},
            {'model': 'DBName', 'label': 'DB Name'},
            {'model': 'DBInformation', 'label': 'DB Information'},
            {'model': 'FeatureName', 'label': 'Feature Name'},
            {'model': 'FeatureDBImpact', 'label': 'Database Impact by Feature'},
            {'model': 'FeatureCPUImpact', 'label': 'CPU Impact by Feature'},
            {'model': 'CallType', 'label': 'Call Type'},
            {'model': 'CallCost', 'label': 'Call Cost'},
            {'model': 'CounterCostName', 'label': 'Counter Cost Name'},
            {'model': 'CounterCost', 'label': 'Counter Cost'},
        ),},

        {'app': 'project', 'label': 'Project', 'models': (
            {'model': 'Project', 'label': 'Project'},
            {'model': 'ProjectInformation', 'label': 'Project Information'},
            {'model': 'TrafficInformation', 'label': 'Traffic Information'},
            {'model': 'FeatureConfiguration', 'label': 'FeatureConfiguration'},
            {'model': 'CounterConfiguration', 'label': 'Counter Configuration'},
            {'model': 'CallTypeCounterConfiguration', 'label': 'Counter Configuration per Call Type'},
            {'model': 'ApplicationConfiguration', 'label': 'Other Application Configuration'},
            {'model': 'DBConfiguration', 'label': 'Database Configuration'},
            {'model': 'SystemConfiguration', 'label': 'System Configuration'},
            {'model': 'CalculatedResult', 'label': 'Calculated Result'},
            {'model': 'DimensioningResult', 'label': 'Dimensioning Result'},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
            {'model': '', 'label': ''},
        ),},

        {'label': 'Misc', 'models': (

            {'model': 'project.customer', 'label': 'Customer Configuration'},
        ),},

        # {'app': 'project', 'label': 'Project', 'models': ({'model': 'project.Customer', 'label': 'Project'}, 'auth.user', 'auth.group',)},

        # Custom app, with models
        {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group', 'auth.permission')},

        # Cross-linked models with custom name; Hide default icon
        {'label': 'Custom', 'icon':None, 'models': (
            'auth.group',
            {'model': 'auth.user', 'label': 'Staff'}
        )},

        # Custom app, no models (child links)
        {'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},

        # Separator
        '-',

        # Custom app and model with permissions
        {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
            {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
        ]},
    )
}

WSGI_APPLICATION = 'SurepayPET.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','

DECIMAL_SEPARATOR = '.'

NUMBER_GROUPING = (3, 2, 0)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
