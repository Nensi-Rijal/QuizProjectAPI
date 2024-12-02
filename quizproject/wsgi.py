"""
WSGI config for quizproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# Check the environment variable 'ENV' to determine the environment (dev or production)
if os.environ.get('ENV') == 'production':
    # Add your production settings path to the sys.path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set the DJANGO_SETTINGS_MODULE dynamically based on the environment
if os.environ.get('ENV') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizproject.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizproject.settings.dev')

application = get_wsgi_application()
app = application
