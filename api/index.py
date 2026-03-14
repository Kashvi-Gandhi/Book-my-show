import os
import sys
from pathlib import Path

# Ensure the project root (<repo>/bookmyseat) and repo root are on sys.path
# so that 'bookmyseat.settings' can be imported reliably in the Vercel runtime.
PROJECT_ROOT = Path(__file__).resolve().parent.parent / 'bookmyseat'  # outer bookmyseat
REPO_ROOT = PROJECT_ROOT.parent                                       # repo root
for path in (PROJECT_ROOT, REPO_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

from django.core.wsgi import get_wsgi_application

# Vercel expects `app` as the entrypoint for Python functions
app = get_wsgi_application()
