"""wsgi module."""

import os

from django.core import wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionario.settings")
application = wsgi.get_wsgi_application()
