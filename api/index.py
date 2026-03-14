import os
import sys
from pathlib import Path

# Add the Django project package directory to sys.path so imports resolve correctly.
# In this repo, the Django project lives at <repo>/bookmyseat/bookmyseat.
ROOT_DIR = Path(__file__).resolve().parent.parent
DJANGO_PROJECT_DIR = ROOT_DIR / 'bookmyseat'
sys.path.insert(0, str(DJANGO_PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

from vercel_django import handler