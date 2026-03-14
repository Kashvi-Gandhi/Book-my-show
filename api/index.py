import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bookmyseat'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

from vercel_django import handler