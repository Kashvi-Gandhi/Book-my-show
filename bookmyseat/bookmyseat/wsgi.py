"""
WSGI config for bookmyseat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Make sure the package dir, project root (<repo>/bookmyseat), and repo root are on sys.path.
PACKAGE_DIR = Path(__file__).resolve().parent          # bookmyseat/bookmyseat
PROJECT_ROOT = PACKAGE_DIR.parent                     # outer bookmyseat folder
REPO_ROOT = PROJECT_ROOT.parent                       # repo root
for path in (PACKAGE_DIR, PROJECT_ROOT, REPO_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

application = get_wsgi_application()
app = application
