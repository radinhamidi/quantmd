#coding=utf-8
import os.path
import sys

LINUX = sys.platform.startswith('linux')
MAC = sys.platform.startswith('darwin')
WINDOWS = sys.platform.startswith('win32')

APP_URL = 'http://localhost:8000/'
LOGIN_URL = APP_URL + 'account/login/' 

if WINDOWS:
    MEDIA_ROOT = 'c:/media/quantmd/'
elif MAC:
    MEDIA_ROOT = '/home/media/quantmd/'
else:
    MEDIA_ROOT = '/home/media/quantmd/'

STATIC_URL = APP_URL + 'static/'
MEDIA_URL = APP_URL + 'media/'


if 'test' in sys.argv:  #Make the test much faster to put sqlite3 database in memory
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'quantmd.db',                
            'USER': '',                    
            'PASSWORD': '',                  
            'HOST': '',                     
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'quantmd-dev',                     
            'USER': 'dev',                     
            'PASSWORD': 'q1w2e3',               
            'HOST': '23.20.239.242',                  
            'PORT': '',
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',
        }
    }


try:
    import debug_toolbar #@UnresolvedImport
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
        #'HIDE_DJANGO_SQL': False,
        #'TAG': 'div',
    }
except:
    pass

