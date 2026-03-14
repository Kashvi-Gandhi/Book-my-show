"""
WSGI config for bookmyseat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Ensure the Django project package is on sys.path.
# Vercel runs from the repository root, so we need to add the outer 'bookmyseat' directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

application = get_wsgi_application()
app = application