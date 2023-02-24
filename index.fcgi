#!/home/venv/bin/python3.5
# -*- coding: utf-8 -*-
import os
import sys
activate_this = '/home/dream/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))
cms_path = '/home/www/alumni_portal/'
sys.path.insert(0, cms_path)
os.chdir(cms_path)
# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "alumni_portal.settings"
from django_fastcgi.servers.fastcgi import runfastcgi
from django.core.servers.basehttp import get_internal_wsgi_application
wsgi_application = get_internal_wsgi_application()
runfastcgi(wsgi_application, method="prefork", daemonize="false", minspare=1, maxspare=1, maxchildren=1)