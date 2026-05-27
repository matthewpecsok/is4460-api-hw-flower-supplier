"""WSGI config for the flower supplier project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_supplier.settings")

application = get_wsgi_application()
