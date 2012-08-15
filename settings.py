# coding=utf-8
import os.path
import sys

PRODUCTION = False
DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG

APP_URL = 'http://23.20.201.4/'
PROJECT_ROOT = os.path.dirname(__file__).replace('\\','/') + '/'  #used in webpage tagging
LOGIN_URL = APP_URL + 'account/login/' 

ADMINS = (
    #('Yifu Diao', 'alexdiaochina@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'support@xifenfen.com'
EMAIL_HOST_PASSWORD = 'Eg4> aZGy' 
EMAIL_PORT = 587


if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'quantmd',                    
            'USER': 'root',                     
            'PASSWORD': 'quantmd:cool1',                
            'HOST': '',                   
            'PORT': '',
        }
    }

# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
TIME_ZONE = None

LANGUAGE_CODE = 'en-us'

DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = APP_URL + 'media/'


STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static/').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = APP_URL + 'static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put absolute path here, like "/home/html/static" or "C:/www/django/static".
    os.path.join(os.path.dirname(__file__),'static/').replace('\\','/')
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '06vvg%or3-(v3=jqwrjpo6f!7*7)hstlzcgw*k234hajfzy%*ee'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

#Allow variable like {{MEDIA_URL}}, {{STATIC_URL}} to be used in the template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'main.utils.context_processors.constants', #custom context processor to load constant
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware', #Adds transaction to all views
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'quantmd.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'main',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Django default is False, set it as True, so we can ask user whether he would like to auto login next time.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True 


#Use local setting to override production settings
#Remember this import must be placed at the end of this file to override settings
if not PRODUCTION: 
    try:
        from settings_local import *
    except ImportError, e:
        pass

