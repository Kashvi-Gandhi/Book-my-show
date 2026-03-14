import os
import sys
from pathlib import Path

# Add the Django project package directory to sys.path so imports resolve correctly.
# In this repo, the Django project lives at <repo>/bookmyseat/bookmyseat.
PROJECT_APP_DIR = Path(__file__).resolve().parent.parent / 'bookmyseat'
sys.path.insert(0, str(PROJECT_APP_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

from vercel_django import handler