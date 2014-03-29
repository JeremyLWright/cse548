
import os
import sys
import site

site.addsitedir('/home/ubuntu/robotenv/local/lib/python2.7/site-packages')

sys.path.append('/home/ubuntu/robot/src/robotractor/')
sys.path.append('/home/ubuntu/robot/src/robotractor/robotractor')

os.environ['DJANGO_SETTINGS_MODULE'] = 'robotractor.settings'

activate_env="/home/ubuntu/robotenv/local/bin/activate_this.py"
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



