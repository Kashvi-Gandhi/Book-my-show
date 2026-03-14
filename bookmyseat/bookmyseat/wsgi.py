"""
WSGI config for bookmyseat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Ensure the Django project package (the inner bookmyseat folder) is on sys.path.
# Vercel runs from the repo root, so we add the inner project package directory.
PROJECT_APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_APP_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

application = get_wsgi_application()
app = application