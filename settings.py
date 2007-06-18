# -*- coding:utf-8 -*-
from os.path import join
from settings_local import *

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media', '')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = join(SITE_URL, 'media', '')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media-admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
APPEND_SLASH = True

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates', ''),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tags',
    'tagging',
    'links',
    'events',
    'txts',
    'optics',
    'photoplanet',
    'misc',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)

ABSOLUTE_URL_OVERRIDES = {
    'events.event': lambda o: '/events/%s/%s/' % (o.startdate.strftime('%Y/%m/%d').lower(), o.id) ,
    'txts.txt': lambda o: '/%s/%s/' % (o.section.permalink, o.permalink),
}

# Tags application.
STYLE_URL = join(MEDIA_URL, 'tags', '')

# Skip <h1>, I'll use on titles
RESTRUCTUREDTEXT_FILTER_SETTINGS = {'initial_header_level': 2 }

SECTIONS_WITH_CUST_TMPL=['blog',]
