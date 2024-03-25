"""
WSGI config for MainCalculator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

settings_module = 'MainCalculator.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'MainCalculator.settings'
# settings_module = 'MainCalculator.deployment'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

