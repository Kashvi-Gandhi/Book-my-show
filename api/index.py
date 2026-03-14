import os
import sys
from pathlib import Path

# Add the project root to the path so Django can be imported
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

from vercel_django import handler