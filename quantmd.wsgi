import os
import sys
sys.path.append('/var/www/quantmd')
sys.path.append('/var/www')

os.environ['DJANGO_SETTINGS_MODULE'] = 'quantmd.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
